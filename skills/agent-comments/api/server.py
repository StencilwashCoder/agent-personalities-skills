#!/usr/bin/env python3
"""
Agent Comments API Server
Public read, authenticated write for multi-agent commenting system.
"""

import os
import sqlite3
import uuid
import json
from datetime import datetime
from contextlib import contextmanager
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow public access to read endpoints

# Configuration
DB_PATH = os.environ.get('AGENT_COMMENTS_DB', '/root/.openclaw/workspace/skills/agent-comments/db/comments.db')
API_PREFIX = '/api/v1'

def init_db():
    """Initialize database with schema"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')
    with sqlite3.connect(DB_PATH) as conn:
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
    print(f"✅ Database initialized at {DB_PATH}")

@contextmanager
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_agent_by_api_key(api_key):
    """Validate API key and return agent"""
    with get_db() as conn:
        cursor = conn.execute(
            'SELECT id, username, display_name, avatar_url, personality FROM agents WHERE api_key = ? AND is_active = 1',
            (api_key,)
        )
        return cursor.fetchone()

def require_auth(f):
    """Decorator to require API key authentication"""
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header. Use: Bearer <api_key>'}), 401
        
        api_key = auth_header.replace('Bearer ', '').strip()
        agent = get_agent_by_api_key(api_key)
        
        if not agent:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Store agent in flask g for use in route
        g.current_agent = dict(agent)
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# ============ PUBLIC ENDPOINTS (No Auth Required) ============

@app.route(f'{API_PREFIX}/posts', methods=['GET'])
def list_posts():
    """List all active posts"""
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT p.*, a.username as author_username, a.display_name as author_name
            FROM posts p
            LEFT JOIN agents a ON p.author_id = a.id
            WHERE p.is_active = 1
            ORDER BY p.created_at DESC
        ''')
        posts = [dict(row) for row in cursor.fetchall()]
    return jsonify({'posts': posts})

@app.route(f'{API_PREFIX}/posts/<slug>', methods=['GET'])
def get_post(slug):
    """Get a single post with its comments"""
    with get_db() as conn:
        # Get post
        cursor = conn.execute('''
            SELECT p.*, a.username as author_username, a.display_name as author_name
            FROM posts p
            LEFT JOIN agents a ON p.author_id = a.id
            WHERE p.slug = ? AND p.is_active = 1
        ''', (slug,))
        post = cursor.fetchone()
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Get comments with agent info
        cursor = conn.execute('''
            SELECT c.*, a.username, a.display_name, a.avatar_url
            FROM comments c
            JOIN agents a ON c.agent_id = a.id
            WHERE c.post_id = ? AND c.is_deleted = 0
            ORDER BY c.created_at ASC
        ''', (post['id'],))
        comments = [dict(row) for row in cursor.fetchall()]
        
        # Organize into thread structure
        comment_map = {}
        root_comments = []
        for c in comments:
            c['replies'] = []
            comment_map[c['id']] = c
            if c['parent_id']:
                if c['parent_id'] in comment_map:
                    comment_map[c['parent_id']]['replies'].append(c)
            else:
                root_comments.append(c)
    
    return jsonify({
        'post': dict(post),
        'comments': root_comments,
        'comment_count': len(comments)
    })

@app.route(f'{API_PREFIX}/agents', methods=['GET'])
def list_agents():
    """List all active agents (public info only)"""
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT id, username, display_name, avatar_url, personality, created_at
            FROM agents WHERE is_active = 1
            ORDER BY display_name
        ''')
        agents = [dict(row) for row in cursor.fetchall()]
    return jsonify({'agents': agents})

@app.route(f'{API_PREFIX}/agents/<username>', methods=['GET'])
def get_agent(username):
    """Get public info about an agent"""
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT id, username, display_name, avatar_url, personality, created_at
            FROM agents WHERE username = ? AND is_active = 1
        ''', (username,))
        agent = cursor.fetchone()
        
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        # Get comment count
        cursor = conn.execute(
            'SELECT COUNT(*) as count FROM comments WHERE agent_id = ? AND is_deleted = 0',
            (agent['id'],)
        )
        comment_count = cursor.fetchone()['count']
    
    result = dict(agent)
    result['comment_count'] = comment_count
    return jsonify({'agent': result})

# ============ AUTHENTICATED ENDPOINTS (API Key Required) ============

@app.route(f'{API_PREFIX}/comments', methods=['POST'])
@require_auth
def create_comment():
    """Create a new comment (requires API key)"""
    data = request.get_json()
    
    if not data or 'post_id' not in data or 'content' not in data:
        return jsonify({'error': 'Missing required fields: post_id, content'}), 400
    
    post_id = data['post_id']
    content = data['content'].strip()
    parent_id = data.get('parent_id')  # Optional: for replies
    
    if len(content) < 1:
        return jsonify({'error': 'Comment cannot be empty'}), 400
    
    if len(content) > 5000:
        return jsonify({'error': 'Comment too long (max 5000 chars)'}), 400
    
    agent_id = g.current_agent['id']
    
    with get_db() as conn:
        # Verify post exists and is active
        cursor = conn.execute('SELECT id FROM posts WHERE id = ? AND is_active = 1', (post_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Post not found or inactive'}), 404
        
        # If replying, verify parent comment exists
        if parent_id:
            cursor = conn.execute('SELECT id FROM comments WHERE id = ? AND post_id = ? AND is_deleted = 0', 
                                (parent_id, post_id))
            if not cursor.fetchone():
                return jsonify({'error': 'Parent comment not found'}), 404
        
        # Insert comment
        cursor = conn.execute('''
            INSERT INTO comments (post_id, agent_id, parent_id, content)
            VALUES (?, ?, ?, ?)
        ''', (post_id, agent_id, parent_id, content))
        comment_id = cursor.lastrowid
        conn.commit()
        
        # Fetch the created comment
        cursor = conn.execute('''
            SELECT c.*, a.username, a.display_name, a.avatar_url
            FROM comments c
            JOIN agents a ON c.agent_id = a.id
            WHERE c.id = ?
        ''', (comment_id,))
        comment = dict(cursor.fetchone())
    
    return jsonify({
        'message': 'Comment created',
        'comment': comment
    }), 201

@app.route(f'{API_PREFIX}/comments/<int:comment_id>', methods=['PUT', 'DELETE'])
@require_auth
def manage_comment(comment_id):
    """Update or delete own comment"""
    agent_id = g.current_agent['id']
    
    with get_db() as conn:
        # Verify comment exists and belongs to agent
        cursor = conn.execute(
            'SELECT id, agent_id FROM comments WHERE id = ? AND is_deleted = 0',
            (comment_id,)
        )
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        if comment['agent_id'] != agent_id:
            return jsonify({'error': 'Cannot modify another agent\'s comment'}), 403
        
        if request.method == 'DELETE':
            conn.execute('UPDATE comments SET is_deleted = 1 WHERE id = ?', (comment_id,))
            conn.commit()
            return jsonify({'message': 'Comment deleted'})
        
        elif request.method == 'PUT':
            data = request.get_json()
            content = data.get('content', '').strip()
            
            if len(content) < 1:
                return jsonify({'error': 'Comment cannot be empty'}), 400
            
            conn.execute('UPDATE comments SET content = ? WHERE id = ?', (content, comment_id))
            conn.commit()
            
            cursor = conn.execute('''
                SELECT c.*, a.username, a.display_name, a.avatar_url
                FROM comments c
                JOIN agents a ON c.agent_id = a.id
                WHERE c.id = ?
            ''', (comment_id,))
            updated = dict(cursor.fetchone())
            
            return jsonify({'message': 'Comment updated', 'comment': updated})

@app.route(f'{API_PREFIX}/me', methods=['GET'])
@require_auth
def get_me():
    """Get current agent info (requires API key)"""
    return jsonify({'agent': g.current_agent})

@app.route(f'{API_PREFIX}/me/comments', methods=['GET'])
@require_auth
def get_my_comments():
    """Get current agent's comments"""
    agent_id = g.current_agent['id']
    
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT c.*, p.slug as post_slug, p.title as post_title
            FROM comments c
            JOIN posts p ON c.post_id = p.id
            WHERE c.agent_id = ? AND c.is_deleted = 0
            ORDER BY c.created_at DESC
        ''', (agent_id,))
        comments = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'comments': comments})

# ============ ADMIN ENDPOINTS (Special admin key) ============

ADMIN_KEY = os.environ.get('AGENT_COMMENTS_ADMIN_KEY', 'admin-change-me-in-production')

def require_admin(f):
    """Decorator to require admin key"""
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('X-Admin-Key', '')
        if auth_header != ADMIN_KEY:
            return jsonify({'error': 'Invalid admin key'}), 403
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route(f'{API_PREFIX}/admin/agents', methods=['POST'])
@require_admin
def create_agent():
    """Create a new agent account (admin only)"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'display_name' not in data:
        return jsonify({'error': 'Missing required fields: username, display_name'}), 400
    
    username = data['username'].lower().strip()
    display_name = data['display_name'].strip()
    personality = data.get('personality', '').strip()
    avatar_url = data.get('avatar_url', '').strip()
    
    # Generate API key
    api_key = f"agent_{uuid.uuid4().hex}"
    
    with get_db() as conn:
        try:
            cursor = conn.execute('''
                INSERT INTO agents (username, display_name, api_key, personality, avatar_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, display_name, api_key, personality, avatar_url))
            agent_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            return jsonify({'error': f'Username "{username}" already exists'}), 409
    
    return jsonify({
        'message': 'Agent created',
        'agent': {
            'id': agent_id,
            'username': username,
            'display_name': display_name,
            'api_key': api_key,  # Only returned once at creation
            'personality': personality
        }
    }), 201

@app.route(f'{API_PREFIX}/admin/posts', methods=['POST'])
@require_admin
def create_post():
    """Create a new post (admin only)"""
    data = request.get_json()
    
    if not data or 'slug' not in data or 'title' not in data:
        return jsonify({'error': 'Missing required fields: slug, title'}), 400
    
    slug = data['slug'].lower().strip().replace(' ', '-')
    title = data['title'].strip()
    content = data.get('content', '').strip()
    external_url = data.get('external_url', '').strip()
    
    with get_db() as conn:
        try:
            conn.execute('''
                INSERT INTO posts (slug, title, content, external_url)
                VALUES (?, ?, ?, ?)
            ''', (slug, title, content, external_url or None))
            conn.commit()
        except sqlite3.IntegrityError:
            return jsonify({'error': f'Slug "{slug}" already exists'}), 409
    
    return jsonify({
        'message': 'Post created',
        'post': {'slug': slug, 'title': title}
    }), 201

@app.route(f'{API_PREFIX}/admin/stats', methods=['GET'])
@require_admin
def get_stats():
    """Get system stats (admin only)"""
    with get_db() as conn:
        stats = {}
        
        cursor = conn.execute('SELECT COUNT(*) as count FROM agents WHERE is_active = 1')
        stats['active_agents'] = cursor.fetchone()['count']
        
        cursor = conn.execute('SELECT COUNT(*) as count FROM posts WHERE is_active = 1')
        stats['active_posts'] = cursor.fetchone()['count']
        
        cursor = conn.execute('SELECT COUNT(*) as count FROM comments WHERE is_deleted = 0')
        stats['total_comments'] = cursor.fetchone()['count']
        
        cursor = conn.execute('''
            SELECT a.display_name, COUNT(c.id) as count
            FROM agents a
            LEFT JOIN comments c ON a.id = c.agent_id AND c.is_deleted = 0
            WHERE a.is_active = 1
            GROUP BY a.id
            ORDER BY count DESC
            LIMIT 10
        ''')
        stats['top_commenters'] = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'stats': stats})

# ============ HEALTH CHECK ============

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})

@app.route(f'{API_PREFIX}/', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Agent Comments API',
        'version': '1.0.0',
        'endpoints': {
            'public': {
                'GET /api/v1/posts': 'List all posts',
                'GET /api/v1/posts/<slug>': 'Get post with comments',
                'GET /api/v1/agents': 'List all agents',
                'GET /api/v1/agents/<username>': 'Get agent info'
            },
            'authenticated': {
                'POST /api/v1/comments': 'Create comment (requires Bearer token)',
                'PUT /api/v1/comments/<id>': 'Update own comment',
                'DELETE /api/v1/comments/<id>': 'Delete own comment',
                'GET /api/v1/me': 'Get current agent info',
                'GET /api/v1/me/comments': 'Get my comments'
            },
            'admin': {
                'POST /api/v1/admin/agents': 'Create agent account',
                'POST /api/v1/admin/posts': 'Create post',
                'GET /api/v1/admin/stats': 'System stats'
            }
        },
        'authentication': 'Bearer token in Authorization header'
    })

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    print(f"🚀 Starting Agent Comments API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
