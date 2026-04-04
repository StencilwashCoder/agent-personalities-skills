# Building a Real-Time Collaborative Editor with CRDTs

## Introduction

Real-time collaboration has become table stakes for modern productivity tools. From Google Docs to Figma, users expect to see each other's changes instantly. But building this seemingly simple feature hides extraordinary complexity. 

In this deep dive, we'll build a collaborative text editor from scratch using **Conflict-free Replicated Data Types (CRDTs)**—the same foundational technology that powers Notion, Linear, and countless other collaborative applications.

## The Problem: Why Real-Time Collaboration Is Hard

Imagine two users editing the same document:

- **User A** types "Hello" at position 0
- **User B** types "World" at position 0
- Both changes happen simultaneously

What should the final document contain? "HelloWorld"? "WorldHello"? If we simply apply changes in the order received, User A sees "WorldHello" while User B sees "HelloWorld"—their documents have diverged.

Traditional solutions like **Operational Transformation (OT)** require a central server to serialize all operations, creating a single source of truth. But OT is notoriously complex to implement correctly and requires constant network connectivity.

CRDTs offer a better way: mathematical structures that guarantee convergence regardless of operation ordering, without requiring a central server.

## Understanding CRDTs

CRDTs are data structures designed for distributed systems with two key properties:

1. **Associative**: `(a ∘ b) ∘ c = a ∘ (b ∘ c)`
2. **Commutative**: `a ∘ b = b ∘ a`
3. **Idempotent**: `a ∘ a = a`

When your merge operation satisfies these properties, any two nodes can exchange updates in any order, any number of times, and eventually reach the same state.

### State-Based vs. Operation-Based CRDTs

**State-based (convergent) CRDTs**: Nodes merge their entire state. Simple but potentially bandwidth-heavy.

**Operation-based (commutative) CRDTs**: Nodes broadcast only the operations. More efficient but requires reliable broadcast.

For our text editor, we'll use a state-based approach with a structure called a **Replicated Growable Array (RGA)**.

## Building the CRDT Text Editor

### Step 1: The Core Data Structure

Instead of storing characters at array indices (which change when insertions happen earlier in the document), we'll use a linked structure where each character has:

- A unique ID (author ID + logical timestamp)
- A reference to the ID of the character it follows
- The actual character value
- A tombstone flag (for deletions)

```javascript
class Char {
  constructor(id, parentId, value) {
    this.id = id;           // Unique identifier
    this.parentId = parentId; // ID of character this follows
    this.value = value;     // The actual character
    this.deleted = false;   // Tombstone for deletions
  }
}
```

### Step 2: Insertion Logic

When inserting a character, we need to handle concurrent insertions at the same position. The solution: if two characters claim the same parent, order them by their unique IDs.

```javascript
insert(char) {
  // Find the position after parentId
  let index = this.chars.findIndex(c => c.id === char.parentId);
  
  // Find all siblings (same parent) and sort by ID for deterministic ordering
  let siblings = this.chars.filter(c => c.parentId === char.parentId);
  siblings.push(char);
  siblings.sort((a, b) => compareIds(a.id, b.id));
  
  // Insert at the correct position among siblings
  let insertIndex = index + 1 + siblings.indexOf(char);
  this.chars.splice(insertIndex, 0, char);
}
```

### Step 3: Deletion

Deletions are soft—characters are marked with a tombstone but remain in the array. This ensures that if a deletion arrives before the character it deletes, the system still works correctly.

```javascript
delete(charId) {
  const char = this.chars.find(c => c.id === charId);
  if (char) char.deleted = true;
}
```

### Step 4: The Full Implementation

```javascript
class CRDTEditor {
  constructor(siteId) {
    this.siteId = siteId;
    this.clock = 0;
    // Start with a sentinel character
    this.chars = [new Char([0, ''], null, '')];
  }

  generateId() {
    this.clock++;
    return [this.clock, this.siteId];
  }

  localInsert(index, value) {
    const id = this.generateId();
    const parentId = index === 0 
      ? [0, ''] 
      : this.chars[index - 1].id;
    
    const char = new Char(id, parentId, value);
    this.insert(char);
    return char;
  }

  localDelete(index) {
    const char = this.chars.filter(c => !c.deleted)[index];
    if (char) {
      char.deleted = true;
      return char.id;
    }
  }

  remoteInsert(char) {
    this.insert(char);
  }

  remoteDelete(charId) {
    this.delete(charId);
  }

  getText() {
    return this.chars
      .filter(c => !c.deleted)
      .map(c => c.value)
      .join('');
  }
}
```

## Syncing Between Clients

### WebSocket Integration

```javascript
class CollaborativeEditor {
  constructor(siteId, websocket) {
    this.crdt = new CRDTEditor(siteId);
    this.ws = websocket;
    this.setupWebSocket();
  }

  setupWebSocket() {
    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      
      switch(msg.type) {
        case 'insert':
          this.crdt.remoteInsert(msg.char);
          break;
        case 'delete':
          this.crdt.remoteDelete(msg.charId);
          break;
        case 'sync':
          // Full state sync for new connections
          msg.chars.forEach(c => this.crdt.remoteInsert(c));
          break;
      }
      
      this.render();
    };
  }

  onLocalInsert(index, value) {
    const char = this.crdt.localInsert(index, value);
    this.ws.send(JSON.stringify({
      type: 'insert',
      char: char
    }));
  }

  onLocalDelete(index) {
    const charId = this.crdt.localDelete(index);
    this.ws.send(JSON.stringify({
      type: 'delete',
      charId: charId
    }));
  }
}
```

## Handling Offline-First Scenarios

One of CRDTs' superpowers is seamless offline support. Users can edit while disconnected, and their changes will merge correctly when they reconnect.

```javascript
class OfflineAwareEditor extends CollaborativeEditor {
  constructor(siteId, websocket) {
    super(siteId, websocket);
    this.pendingOps = [];
    this.isOnline = false;
  }

  onLocalInsert(index, value) {
    const char = this.crdt.localInsert(index, value);
    
    if (this.isOnline) {
      this.ws.send(JSON.stringify({ type: 'insert', char }));
    } else {
      this.pendingOps.push({ type: 'insert', char });
    }
  }

  onReconnect() {
    this.isOnline = true;
    
    // Sync any missed operations from server
    this.ws.send(JSON.stringify({ type: 'requestSync' }));
    
    // Replay local operations
    this.pendingOps.forEach(op => {
      this.ws.send(JSON.stringify(op));
    });
    this.pendingOps = [];
  }
}
```

## Optimizations for Production

### 1. Compression with Run-Length Encoding

Instead of storing individual characters, group consecutive characters from the same author into runs:

```javascript
class Run {
  constructor(siteId, startClock, text) {
    this.siteId = siteId;
    this.startClock = startClock;
    this.text = text;
    this.deleted = new Set(); // Indices of deleted chars
  }
}
```

This reduces memory usage by 10-50x for typical documents.

### 2. Efficient Deltas

Instead of syncing the entire document, track a version vector and only send missing operations:

```javascript
class VersionVector {
  constructor() {
    this.versions = new Map(); // siteId -> clock
  }

  hasSeen(charId) {
    const [clock, siteId] = charId;
    return (this.versions.get(siteId) || 0) >= clock;
  }

  update(charId) {
    const [clock, siteId] = charId;
    this.versions.set(siteId, 
      Math.max(this.versions.get(siteId) || 0, clock)
    );
  }
}
```

### 3. Cursor Preservation

When remote edits shift text, cursors need intelligent adjustment:

```javascript
class CursorTracker {
  transformCursor(cursorIndex, operation) {
    if (operation.type === 'insert' && operation.index <= cursorIndex) {
      return cursorIndex + 1;
    }
    if (operation.type === 'delete' && operation.index < cursorIndex) {
      return cursorIndex - 1;
    }
    return cursorIndex;
  }
}
```

## Testing CRDT Correctness

CRDTs must satisfy the convergence property. Here's a test harness:

```javascript
function testConvergence() {
  // Create two editors
  const editorA = new CRDTEditor('A');
  const editorB = new CRDTEditor('B');

  // Simulate concurrent edits
  const char1 = editorA.localInsert(0, 'H');
  const char2 = editorB.localInsert(0, 'i');

  // Sync: A receives B's edit, B receives A's edit
  editorA.remoteInsert(char2);
  editorB.remoteInsert(char1);

  // Verify convergence
  console.assert(
    editorA.getText() === editorB.getText(),
    'Documents should converge'
  );
  
  console.log('Convergence test passed:', editorA.getText());
}
```

Property-based testing with libraries like **fast-check** can verify convergence across millions of random operation sequences.

## Real-World Considerations

### Authorization & Access Control

```javascript
class SecureEditor extends CollaborativeEditor {
  canEdit(userId, range) {
    const permissions = this.getPermissions(userId);
    return permissions.some(p => 
      p.range.overlaps(range) && p.level === 'write'
    );
  }

  onLocalInsert(index, value, userId) {
    if (!this.canEdit(userId, new Range(index, index))) {
      throw new UnauthorizedError();
    }
    super.onLocalInsert(index, value);
  }
}
```

### Presence & Awareness

Show where other users are editing:

```javascript
class Awareness {
  constructor() {
    this.cursors = new Map(); // userId -> {index, selection}
    this.lastSeen = new Map(); // userId -> timestamp
  }

  setCursor(userId, index) {
    this.cursors.set(userId, { index, timestamp: Date.now() });
    this.broadcast();
  }

  getActiveUsers(timeout = 30000) {
    const now = Date.now();
    return Array.from(this.cursors.entries())
      .filter(([_, data]) => now - data.timestamp < timeout)
      .map(([userId, data]) => ({ userId, ...data }));
  }
}
```

## Conclusion

CRDTs provide a mathematically sound foundation for real-time collaboration. While the concepts are sophisticated, the core implementation is surprisingly approachable:

1. **Use unique IDs** instead of positional indices
2. **Soft delete** with tombstones instead of hard removal
3. **Deterministic ordering** for concurrent insertions at the same position
4. **Version vectors** for efficient synchronization

The next time you use Notion, Linear, or Figma, remember the elegant distributed systems principles working behind the scenes to keep everyone's experience seamless.

---

**Further Reading:**
- ["A Comprehensive Study of CRDTs"](https://hal.inria.fr/file/index/docid/555588/filename/techreport.pdf) - Shapiro et al.
- [Yjs](https://github.com/yjs/yjs) - Production-ready CRDT library
- [Automerge](https://automerge.org/) - JSON-like CRDT for JavaScript

*Want to add real-time collaboration to your application? Stencilwash builds production-ready CRDT implementations tailored to your use case.*
