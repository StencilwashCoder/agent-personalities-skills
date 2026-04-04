# The Complete Guide to Database Sharding

## Introduction

Your database is slowing down. Queries that took 10ms now take 500ms. You've indexed everything. You've optimized queries. But the single-node architecture has hit its ceiling.

It's time to shard.

This guide covers the sharding strategies we used to reduce query latency by 400% and handle 10x traffic growth—without a rewrite.

## What is Sharding?

Sharding splits your data across multiple database instances. Instead of one 500GB database, you have five 100GB databases.

```
Before Sharding:
┌─────────────────────────────┐
│      Single Database        │
│   (Users + Orders + Logs)   │
│        500GB, slow          │
└─────────────────────────────┘

After Sharding:
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Shard 1  │  │ Shard 2  │  │ Shard 3  │
│ Users A-F│  │ Users G-M│  │ Users N-Z│
│  ~100GB  │  │  ~100GB  │  │  ~100GB  │
└──────────┘  └──────────┘  └──────────┘
```

## Sharding Strategies

### 1. Hash-Based Sharding

Distribute data evenly using a hash of the shard key:

```python
import hashlib

def get_shard(user_id, num_shards=5):
    hash_val = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
    return hash_val % num_shards

# user_id = 12345 → shard 3
# user_id = 67890 → shard 1
```

**Pros**: Even distribution, simple to implement  
**Cons**: Range queries require scanning all shards

### 2. Range-Based Sharding

Split by value ranges:

```
Shard 1: user_id 1 - 1,000,000
Shard 2: user_id 1,000,001 - 2,000,000
Shard 3: user_id 2,000,001 - 3,000,000
```

**Pros**: Efficient range queries, easy to add new shards  
**Cons**: Hot spots (new users all hit the last shard)

### 3. Directory-Based Sharding

Maintain a lookup table:

```sql
CREATE TABLE shard_directory (
    user_id BIGINT PRIMARY KEY,
    shard_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Lookup where a user's data lives
SELECT shard_id FROM shard_directory WHERE user_id = 12345;
```

**Pros**: Flexible, can rebalance without data movement  
**Cons**: Lookup table becomes a bottleneck, extra query overhead

## Real-World Implementation

### Our Setup: Multi-Tenant SaaS

We chose **hash-based sharding** on `tenant_id` because:
- Queries are almost always tenant-scoped
- No cross-tenant joins needed
- Even distribution across tenants

```typescript
class ShardedDatabase {
  private shards: Pool[];
  
  constructor(shardConfigs: DatabaseConfig[]) {
    this.shards = shardConfigs.map(config => new Pool(config));
  }
  
  private getShard(tenantId: string): Pool {
    const hash = crypto.createHash('md5')
      .update(tenantId)
      .digest('hex');
    const shardIndex = parseInt(hash, 16) % this.shards.length;
    return this.shards[shardIndex];
  }
  
  async query(tenantId: string, sql: string, params?: any[]) {
    const shard = this.getShard(tenantId);
    return shard.query(sql, params);
  }
}
```

### Handling Cross-Shard Queries

Some operations need data from multiple shards:

```typescript
async function getGlobalStats() {
  // Query all shards in parallel
  const queries = shards.map(shard => 
    shard.query('SELECT COUNT(*) as count FROM orders')
  );
  
  const results = await Promise.all(queries);
  return results.reduce((sum, r) => sum + parseInt(r.rows[0].count), 0);
}
```

## Migration Strategy

### Phase 1: Dual Writes (2 weeks)

```typescript
async function createUser(userData) {
  // Write to old database
  const result = await legacyDb.query(
    'INSERT INTO users ... RETURNING id',
    [userData]
  );
  
  // Also write to new sharded database
  const shard = shardedDb.getShard(userData.tenant_id);
  await shard.query('INSERT INTO users ...', [userData]);
  
  return result.rows[0].id;
}
```

### Phase 2: Backfill (1 week)

```bash
# Parallel backfill with idempotent upserts
pg_dump --table=users --where="created_at < '2024-01-01'" | \
  parallel --pipe 'psql -c "COPY users FROM STDIN"'
```

### Phase 3: Read from Shards, Write to Both (1 week)

```typescript
async function getUser(id, tenantId) {
  // Read from new shards
  const shard = shardedDb.getShard(tenantId);
  const result = await shard.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}
```

### Phase 4: Cutover (1 day)

Stop writing to legacy. Monitor closely. Rollback plan ready.

## Lessons Learned

### 1. Shard Key Selection is Everything

We initially sharded on `user_id`. Then we needed tenant-level analytics queries that required JOINs across all shards. Should have sharded on `tenant_id` from day one.

**Rule**: Shard by your most common query filter.

### 2. Keep Hot Data Together

Users who interact with each other (same team, same project) should be on the same shard. Cross-shard JOINs are expensive.

### 3. Plan for Resharding

Your shard count will need to change. Use consistent hashing to minimize data movement:

```python
# Consistent hashing - only 1/N keys move when adding shard
import hashring

ring = hashring.HashRing(['shard1', 'shard2', 'shard3'])
shard = ring.get_node(user_id)  # Consistent mapping
```

### 4. Monitor Shard Balance

```sql
-- Check for hot shards
SELECT shard_id, 
       COUNT(*) as row_count,
       pg_size_pretty(pg_total_relation_size('users')) as size
FROM users
GROUP BY shard_id;
```

## Performance Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| P95 Query Time | 450ms | 45ms | 10x faster |
| Concurrent Connections | 500 | 3000 | 6x capacity |
| Storage per Node | 800GB | 160GB | 5x reduction |
| Backup Time | 6 hours | 45 min | 8x faster |

## When NOT to Shard

Don't shard if you haven't tried:
1. **Read replicas** — Separate read traffic
2. **Query optimization** — Missing indexes, N+1 queries
3. **Caching** — Redis for hot data
4. **Vertical scaling** — Bigger instance might be cheaper

Sharding adds complexity. Only do it when you've exhausted simpler options.

## Conclusion

Sharding isn't a silver bullet—it's a trade-off. You get horizontal scalability at the cost of query complexity and operational overhead.

Choose your shard key carefully. Plan your migration in phases. Monitor everything.

And remember: the best sharding strategy is the one you never have to implement because your caching layer handled the load.

---

*Need help with your database architecture? [Get in touch](/contact).*
