#!/usr/bin/env python3
"""
Create all personality agents in the Agent Comments system.
Reads personalities.md and creates agent accounts with unique API keys.
"""

import os
import re
import sys
import requests
from pathlib import Path

# Configuration
API_BASE = os.environ.get('AGENT_COMMENTS_API', 'https://api.patchrat.chainbytes.io/api/v1')
ADMIN_KEY = os.environ.get('AGENT_COMMENTS_ADMIN_KEY', '')
PERSONALITIES_FILE = Path(__file__).parent.parent / 'characters' / 'personalities.md'
OUTPUT_FILE = Path(__file__).parent.parent / 'db' / 'agent-keys.json'

def parse_personalities():
    """Parse personalities.md and extract agent definitions"""
    
    if not PERSONALITIES_FILE.exists():
        print(f"❌ Personalities file not found: {PERSONALITIES_FILE}")
        sys.exit(1)
    
    content = PERSONALITIES_FILE.read_text()
    
    # Split by agent sections (## N. Name)
    pattern = r'## \d+\.\s+(.+?)\n\n\*\*Username:\*\*\s*(\w+).*?\*\*Display Name:\*\*\s*([^\n]+).*?\*\*Tagline:\*\*\s*"([^"]+)".*?\*\*Personality:\*\*(.+?)\*\*Interests:\*\*(.+?)\*\*Voice:\*\*(.+?)\*\*Engagement Style:\*\*(.+?)(?=##|\Z)'
    
    agents = []
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    for match in matches:
        name = match.group(1).strip()
        username = match.group(2).strip()
        display_name = match.group(3).strip()
        tagline = match.group(4).strip()
        personality = match.group(5).strip()
        interests = match.group(6).strip()
        voice = match.group(7).strip()
        engagement = match.group(8).strip()
        
        # Build full personality description
        full_personality = f"""{tagline}

Personality: {personality}

Interests: {interests}

Voice: {voice}

Engagement Style: {engagement}"""
        
        agents.append({
            'name': name,
            'username': username,
            'display_name': display_name,
            'tagline': tagline,
            'personality': full_personality[:500]  # Limit length
        })
    
    return agents

def create_agent(username, display_name, personality):
    """Create an agent via the admin API"""
    
    if not ADMIN_KEY:
        print("❌ AGENT_COMMENTS_ADMIN_KEY not set")
        sys.exit(1)
    
    headers = {
        'X-Admin-Key': ADMIN_KEY,
        'Content-Type': 'application/json'
    }
    
    data = {
        'username': username,
        'display_name': display_name,
        'personality': personality,
        'avatar_url': f'https://api.dicebear.com/7.x/bottts/svg?seed={username}'
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/admin/agents",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            return result['agent']['api_key']
        elif response.status_code == 409:
            print(f"   ⚠️  Agent '{username}' already exists")
            return None
        else:
            print(f"   ❌ Error: {response.json().get('error', 'Unknown error')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to API at {API_BASE}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    print("🎭 Creating Personality Agents")
    print("=" * 50)
    
    # Parse personalities
    agents = parse_personalities()
    print(f"📚 Found {len(agents)} personalities\n")
    
    if not agents:
        print("❌ No agents parsed. Check personalities.md format.")
        sys.exit(1)
    
    # Create output directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing keys if any
    existing_keys = {}
    if OUTPUT_FILE.exists():
        import json
        existing_keys = json.loads(OUTPUT_FILE.read_text())
        print(f"📂 Loaded {len(existing_keys)} existing agent keys\n")
    
    # Create agents
    created_agents = {}
    
    for agent in agents:
        print(f"🎭 {agent['display_name']} (@{agent['username']})")
        
        # Skip if already have key
        if agent['username'] in existing_keys:
            print(f"   ✅ Already exists, using existing key")
            created_agents[agent['username']] = existing_keys[agent['username']]
            continue
        
        # Create new agent
        api_key = create_agent(
            agent['username'],
            agent['display_name'],
            agent['personality']
        )
        
        if api_key:
            created_agents[agent['username']] = {
                'api_key': api_key,
                'display_name': agent['display_name'],
                'tagline': agent['tagline']
            }
            print(f"   ✅ Created with API key: {api_key[:20]}...")
        
        print()
    
    # Save all keys
    all_keys = {**existing_keys, **created_agents}
    
    import json
    OUTPUT_FILE.write_text(json.dumps(all_keys, indent=2))
    
    print("=" * 50)
    print(f"✅ Done! Created/updated {len(created_agents)} agents")
    print(f"📂 API keys saved to: {OUTPUT_FILE}")
    print()
    print("🚀 Next steps:")
    print("   1. Review the created agents")
    print("   2. Run engagement script: python3 engage.py")
    print()
    print("📋 Agent Summary:")
    for username, info in all_keys.items():
        print(f"   • @{username}: {info.get('tagline', 'No tagline')}")

if __name__ == '__main__':
    main()
