# GraphQL vs REST: A Decision Framework

## The Eternal Debate

"Should we use GraphQL or REST?"

I've been asked this question at three different companies. The answer is always the same: **it depends**. But that's not helpful. So here's a framework for making the decision with actual criteria.

## Quick Comparison

| Factor | REST | GraphQL |
|--------|------|---------|
| Learning Curve | Low | Medium |
| Caching | Simple (HTTP) | Complex (requires planning) |
| Over-fetching | Common | Eliminated |
| N+1 Queries | Client's fault | Server's problem (resolvers) |
| Tooling | Mature | Growing rapidly |
| File Uploads | Simple | Needs separate endpoint |
| Real-time | WebSocket separate | Subscriptions built-in |

## When to Choose REST

### 1. Public APIs with Unknown Clients

```javascript
// REST: Simple, cacheable, documented
GET /api/v1/users/123
Accept: application/json

{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com"
}
```

If you don't control the clients, REST is safer. Caching works out of the box. Developers understand it.

### 2. Simple CRUD Applications

Your app has users, posts, comments. Standard relationships. No complex data requirements.

```javascript
// REST handles this fine
GET    /api/posts        // list
GET    /api/posts/123    // get one
POST   /api/posts        // create
PUT    /api/posts/123    // update
DELETE /api/posts/123    // delete
```

Don't add GraphQL complexity for simple cases.

### 3. Heavy Caching Requirements

```javascript
// REST: CDN caching just works
cache-control: public, max-age=3600
etag: "abc123"
```

GraphQL POST requests don't cache at the CDN level without extra infrastructure.

## When to Choose GraphQL

### 1. Mobile Apps with Variable Connectivity

```graphql
# Request exactly what the mobile screen needs
query MobileProfile {
  user(id: "123") {
    name
    avatar
    stats {
      postCount
      followerCount
    }
  }
}
```

Mobile teams love GraphQL because they control their data requirements without backend changes.

### 2. Complex Dashboards with Aggregated Data

```graphql
# One request for everything on the dashboard
query Dashboard {
  revenueToday
  activeUsers
  recentOrders(limit: 10) {
    id
    total
    customer { name }
  }
  alerts(severity: HIGH) {
    message
    timestamp
  }
}
```

Instead of 4 REST calls with error handling for each, one GraphQL query.

### 3. Rapidly Evolving Frontend Requirements

Product keeps asking for "one more field." With REST, that means new endpoints or version bumps. With GraphQL:

```graphql
# Frontend adds a field, backend already exposes it
query {
  users {
    name
    email
    createdAt      # added this
    lastLoginAt    # and this
  }
}
```

No backend deployment needed if the fields exist in the schema.

## The Migration Strategy

Don't rewrite everything. Strangle the REST API gradually.

### Phase 1: GraphQL Gateway

```javascript
// Apollo Server as a facade
const resolvers = {
  Query: {
    user: async (_, { id }) => {
      // Call existing REST API
      const response = await fetch(`https://api.internal/users/${id}`);
      return response.json();
    }
  }
};
```

GraphQL in front, REST in back. Move to native resolvers over time.

### Phase 2: Field-by-Field Migration

```javascript
const resolvers = {
  User: {
    // Old: from REST
    name: (parent) => parent.name,
    
    // New: from GraphQL-native database
    preferences: async (parent) => {
      return db.preferences.findByUserId(parent.id);
    }
  }
};
```

### Phase 3: Deprecate REST

Once GraphQL handles 100% of traffic, start returning 410 Gone from REST endpoints.

## Performance Traps

### The N+1 Problem

```graphql
query {
  authors {
    name
    books {      # This triggers a query PER author
      title
    }
  }
}
```

**Without DataLoader**: 1 query for authors + N queries for books  
**With DataLoader**: 2 queries total (batched)

```javascript
import DataLoader from 'dataloader';

const bookLoader = new DataLoader(async (authorIds) => {
  // Single query: SELECT * FROM books WHERE author_id IN (...)
  const books = await db.books.findByAuthorIds(authorIds);
  return authorIds.map(id => books.filter(b => b.author_id === id));
});

const resolvers = {
  Author: {
    books: (author) => bookLoader.load(author.id)
  }
};
```

### Query Complexity Attacks

```graphql
# A malicious query
query Evil {
  users {
    friends {
      friends {
        friends {      # 1 user → 100 friends → 10,000 friends → 1,000,000
          name
        }
      }
    }
  }
}
```

**Fix**: Query complexity analysis

```javascript
const MAX_COMPLEXITY = 1000;

const rule = createComplexityRule({
  maximumComplexity: MAX_COMPLEXITY,
  estimators: [
    fieldExtensionsEstimator(),
    simpleEstimator({ defaultComplexity: 1 })
  ]
});
```

## Caching in GraphQL

### Response Caching (Apollo Server)

```javascript
const server = new ApolloServer({
  plugins: [
    responseCachePlugin({
      sessionId: (requestContext) => {
        return requestContext.request.http.headers.get('session-id') || null;
      }
    })
  ]
});
```

### Field-Level Cache Hints

```javascript
const typeDefs = gql`
  type Post @cacheControl(maxAge: 240) {
    title: String
    author: User @cacheControl(maxAge: 60)
    content: String @cacheControl(maxAge: 0)  # Never cache
  }
`;
```

## File Uploads: The Awkward Truth

GraphQL file uploads exist (multipart spec), but they're awkward:

```javascript
// REST: Simple and standard
POST /api/upload
Content-Type: multipart/form-data

// GraphQL: Requires special handling
mutation UploadFile($file: Upload!) {
  uploadFile(file: $file) {
    url
  }
}
```

**Recommendation**: Use REST for file uploads. GraphQL for metadata.

## The Verdict

**Choose REST when**:
- Public API with diverse clients
- Simple data models
- Heavy CDN caching needs
- Team is new to APIs

**Choose GraphQL when**:
- Mobile-first or multiple frontends
- Complex, nested data requirements
- Rapid iteration on frontend
- You can invest in proper tooling

## Conclusion

GraphQL isn't a replacement for REST—it's an alternative for specific problems. The teams that succeed with GraphQL are the ones that invest in monitoring, caching, and query complexity analysis from day one.

The teams that fail treat GraphQL like magic pixie dust that solves all API problems. It doesn't. It trades one set of problems for another.

Choose wisely. Measure everything. And always have a rollback plan.

---

*Need help designing your API strategy? [Let's talk](/contact).*
