#!/usr/bin/env python3
"""
Create a new blog post (admin only)
"""

import os
import sys
import argparse
import requests

API_URL = os.environ.get('AGENT_COMMENTS_API', 'http://localhost:5000/api/v1')
ADMIN_KEY = os.environ.get('AGENT_COMMENTS_ADMIN_KEY', 'admin-change-me-in-production')

def create_post(slug, title, content=None, external_url=None):
    headers = {
        'X-Admin-Key': ADMIN_KEY,
        'Content-Type': 'application/json'
    }
    
    data = {
        'slug': slug,
        'title': title,
    }
    
    if content:
        data['content'] = content
    if external_url:
        data['external_url'] = external_url
    
    try:
        response = requests.post(
            f"{API_URL}/admin/posts",
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Post created: {result['post']['title']}")
            print(f"   Slug: {result['post']['slug']}")
            print(f"   URL: {API_URL.replace('/api/v1', '')}/posts/{result['post']['slug']}")
        elif response.status_code == 409:
            print(f"❌ Error: Slug '{slug}' already exists")
        else:
            print(f"❌ Error: {response.json().get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("   Make sure the server is running: python3 api/server.py")

def main():
    parser = argparse.ArgumentParser(description='Create a new blog post')
    parser.add_argument('--slug', '-s', required=True, help='URL slug (lowercase, no spaces)')
    parser.add_argument('--title', '-t', required=True, help='Post title')
    parser.add_argument('--content', '-c', help='Post content (optional)')
    parser.add_argument('--external-url', '-u', help='External URL if post lives elsewhere')
    
    args = parser.parse_args()
    
    create_post(args.slug, args.title, args.content, args.external_url)

if __name__ == '__main__':
    main()
