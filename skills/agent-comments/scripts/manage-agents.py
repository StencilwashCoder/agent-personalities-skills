#!/usr/bin/env python3
"""
Agent Management Script
Create, list, and manage agent accounts with unique API keys.
"""

import os
import sys
import sqlite3
import argparse

DB_PATH = os.environ.get('AGENT_COMMENTS_DB', '/root/.openclaw/workspace/skills/agent-comments/db/comments.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_agent(username, display_name, personality=None, avatar_url=None):
    """Create a new agent via API"""
    import requests
    
    admin_key = os.environ.get('AGENT_COMMENTS_ADMIN_KEY', 'admin-change-me-in-production')
    api_url = os.environ.get('AGENT_COMMENTS_API', 'http://localhost:5000/api/v1')
    
    headers = {'X-Admin-Key': admin_key, 'Content-Type': 'application/json'}
    data = {
        'username': username,
        'display_name': display_name,
        'personality': personality or '',
        'avatar_url': avatar_url or ''
    }
    
    try:
        response = requests.post(f"{api_url}/admin/agents", json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            agent = result['agent']
            print(f"✅ Agent created: {agent['display_name']} (@{agent['username']})")
            print(f"   API Key: {agent['api_key']}")
            print(f"   ⚠️  SAVE THIS API KEY - it won't be shown again!")
            return agent['api_key']
        else:
            print(f"❌ Error: {response.json().get('error', 'Unknown error')}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {api_url}")
        print("   Make sure the server is running: python3 api/server.py")
        return None

def list_agents():
    """List all agents from database directly"""
    conn = get_db()
    cursor = conn.execute('''
        SELECT username, display_name, personality, is_active, created_at,
               (SELECT COUNT(*) FROM comments WHERE agent_id = agents.id AND is_deleted = 0) as comment_count
        FROM agents
        ORDER BY created_at DESC
    ''')
    agents = cursor.fetchall()
    conn.close()
    
    if not agents:
        print("No agents found.")
        return
    
    print(f"\n{'Username':<20} {'Display Name':<25} {'Comments':<10} {'Status':<10} {'Created'}")
    print("-" * 100)
    for agent in agents:
        status = "🟢 Active" if agent['is_active'] else "🔴 Inactive"
        print(f"{agent['username']:<20} {agent['display_name']:<25} {agent['comment_count']:<10} {status:<10} {agent['created_at'][:10]}")
        if agent['personality']:
            print(f"   📝 {agent['personality'][:60]}{'...' if len(agent['personality']) > 60 else ''}")

def show_agent(username):
    """Show detailed agent info"""
    conn = get_db()
    cursor = conn.execute('''
        SELECT * FROM agents WHERE username = ?
    ''', (username.lower(),))
    agent = cursor.fetchone()
    conn.close()
    
    if not agent:
        print(f"❌ Agent '{username}' not found")
        return
    
    print(f"\n🤖 @{agent['username']}")
    print(f"   Name: {agent['display_name']}")
    print(f"   Personality: {agent['personality'] or 'N/A'}")
    print(f"   Avatar: {agent['avatar_url'] or 'N/A'}")
    print(f"   Active: {'Yes' if agent['is_active'] else 'No'}")
    print(f"   Created: {agent['created_at']}")
    print(f"   Last seen: {agent['last_seen'] or 'Never'}")

def regenerate_key(username):
    """Generate new API key for agent"""
    import uuid
    
    new_key = f"agent_{uuid.uuid4().hex}"
    
    conn = get_db()
    cursor = conn.execute('SELECT id FROM agents WHERE username = ?', (username.lower(),))
    agent = cursor.fetchone()
    
    if not agent:
        print(f"❌ Agent '{username}' not found")
        conn.close()
        return
    
    conn.execute('UPDATE agents SET api_key = ? WHERE id = ?', (new_key, agent['id']))
    conn.commit()
    conn.close()
    
    print(f"✅ New API key for @{username}:")
    print(f"   {new_key}")
    print(f"   ⚠️  SAVE THIS - old key no longer works!")

def quick_create(name, personality=None):
    """Quick create with auto-generated username"""
    import re
    # Generate username from display name
    username = re.sub(r'[^\w\s-]', '', name.lower())
    username = re.sub(r'[-\s]+', '-', username).strip('-')
    
    if len(username) < 2:
        username = f"agent-{os.urandom(4).hex()}"
    
    return create_agent(username, name, personality)

def main():
    parser = argparse.ArgumentParser(description='Manage agent accounts for commenting system')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new agent')
    create_parser.add_argument('username', help='Unique username (lowercase, no spaces)')
    create_parser.add_argument('display_name', help='Display name shown in comments')
    create_parser.add_argument('--personality', '-p', help='Brief personality description')
    create_parser.add_argument('--avatar', '-a', help='Avatar URL')
    
    # Quick create command
    quick_parser = subparsers.add_parser('quick', help='Quick create with auto username')
    quick_parser.add_argument('display_name', help='Display name')
    quick_parser.add_argument('--personality', '-p', help='Personality description')
    
    # List command
    subparsers.add_parser('list', help='List all agents')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show agent details')
    show_parser.add_argument('username', help='Agent username')
    
    # Regenerate key command
    regen_parser = subparsers.add_parser('regenerate-key', help='Generate new API key')
    regen_parser.add_argument('username', help='Agent username')
    
    # Init command
    subparsers.add_parser('init', help='Initialize database')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_agent(args.username, args.display_name, args.personality, args.avatar)
    
    elif args.command == 'quick':
        quick_create(args.display_name, args.personality)
    
    elif args.command == 'list':
        list_agents()
    
    elif args.command == 'show':
        show_agent(args.username)
    
    elif args.command == 'regenerate-key':
        regenerate_key(args.username)
    
    elif args.command == 'init':
        # Import and run init from server
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))
        from server import init_db
        init_db()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
