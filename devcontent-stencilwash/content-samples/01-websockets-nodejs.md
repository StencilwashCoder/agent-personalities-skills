# Building Real-Time APIs with WebSockets and Node.js

## Introduction

When your users expect instant updates—live chat, real-time dashboards, collaborative editing—you need more than HTTP polling. You need persistent connections. You need WebSockets.

But scaling WebSockets is where most teams hit a wall. This guide walks through production-tested patterns for building WebSocket APIs that handle millions of concurrent connections without falling over.

## Why WebSockets?

HTTP request/response is simple but inefficient for real-time scenarios:

- **Polling wastes resources** — constant HTTP requests, most returning "no new data"
- **Latency stacks up** — 100ms round-trip × 10 polls/second = unnecessary delay
- **Server load compounds** — each poll creates a new TCP connection

WebSockets solve this with a single persistent TCP connection that stays open for bidirectional communication.

```javascript
// HTTP Polling (wasteful)
setInterval(() => {
  fetch('/api/messages')  // New TCP connection every time
    .then(res => res.json())
    .then(messages => render(messages));
}, 1000);

// WebSocket (efficient)
const ws = new WebSocket('wss://api.example.com');
ws.onmessage = (event) => render(JSON.parse(event.data));  // One connection
```

## The Architecture

### Basic Setup with ws Library

```javascript
import { WebSocketServer } from 'ws';
import http from 'http';

const server = http.createServer();
const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
  console.log('New connection:', req.socket.remoteAddress);
  
  ws.on('message', (data) => {
    // Handle incoming message
    handleMessage(ws, data);
  });
  
  ws.on('close', () => {
    cleanupConnection(ws);
  });
});

server.listen(8080);
```

Looks simple, right? Now let's make it production-ready.

## Handling Scale: Connection Management

### The Problem

Node.js is single-threaded. One WebSocket server can handle ~10,000 concurrent connections before hitting limits. What happens when you need 100,000? 1,000,000?

### Solution: Redis Adapter + Multiple Nodes

```javascript
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';
import { Server } from 'socket.io';

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

const io = new Server(server);
io.adapter(createAdapter(pubClient, subClient));

// Now messages broadcast across all server instances
io.on('connection', (socket) => {
  socket.on('chat-message', (msg) => {
    // Broadcasts to ALL connected clients across ALL nodes
    io.emit('chat-message', msg);
  });
});
```

### Connection State Recovery

What happens when a user briefly disconnects? Don't make them rejoin everything:

```javascript
const io = new Server(server, {
  connectionStateRecovery: {
    maxDisconnectionDuration: 2 * 60 * 1000,  // 2 minutes
    skipMiddlewares: true,
  }
});
```

## Message Patterns

### Request-Reply Pattern

Sometimes you need to call a method and get a response:

```javascript
// Client
const response = await socket.emitWithAck('get-user', userId);
console.log(response);  // { id: '123', name: 'Alice' }

// Server
socket.on('get-user', async (userId, callback) => {
  const user = await db.users.findById(userId);
  callback(user);
});
```

### Room-Based Broadcasting

Send messages to specific groups without iterating all connections:

```javascript
// Join a room
socket.join(`room:${roomId}`);

// Broadcast to room
io.to(`room:${roomId}`).emit('message', data);

// Leave room
socket.leave(`room:${roomId}`);
```

## Production Checklist

✅ **Use a load balancer with sticky sessions** OR **disable polling fallback**  
✅ **Implement heartbeat/ping-pong** to detect dead connections  
✅ **Set connection limits** per IP to prevent abuse  
✅ **Use Redis adapter** for horizontal scaling  
✅ **Monitor connection metrics** — active, disconnections, message rates  
✅ **Implement proper error handling** — don't crash on malformed messages  
✅ **Rate limit messages** per connection  

## Heartbeat Implementation

```javascript
function heartbeat(ws) {
  ws.isAlive = true;
}

wss.on('connection', (ws) => {
  ws.isAlive = true;
  ws.on('pong', () => heartbeat(ws));
});

// Ping all clients every 30 seconds
const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) return ws.terminate();
    
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);
```

## Performance Benchmarks

On a standard 4-core VPS:
- **Raw WebSocket**: ~50,000 concurrent connections
- **With Socket.IO + Redis**: ~30,000 concurrent connections  
- **With message processing**: ~10,000-15,000 active chat users

For 100,000+ connections: deploy 5+ nodes behind a load balancer with Redis adapter.

## Conclusion

WebSockets aren't magic—they're just persistent TCP connections. The complexity comes from handling failure modes: reconnections, dropped messages, server restarts, and scaling beyond single-node limits.

Start simple. Add Redis when you need multiple nodes. Monitor everything. And never trust the client.

---

*Need help scaling your real-time features? [Let's talk](/contact).*
