#!/usr/bin/env python3
"""
Agent Engagement Engine
Randomly selects agents to engage with blog posts, maintaining conversation threads.
"""

import os
import sys
import json
import random
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
API_BASE = os.environ.get('AGENT_COMMENTS_API', 'https://api.patchrat.chainbytes.io/api/v1')
AGENT_KEYS_FILE = Path(__file__).parent.parent / 'db' / 'agent-keys.json'
PERSONALITIES_FILE = Path(__file__).parent.parent / 'characters' / 'personalities.md'

# Minimum time between comments from same agent (minutes)
MIN_COOLDOWN = int(os.environ.get('AGENT_COOLDOWN_MINUTES', '30'))

class AgentEngager:
    """Manages agent engagement with posts and threads"""
    
    def __init__(self):
        self.agents = self.load_agents()
        self.last_comment_times = {}  # Track when each agent last commented
        
    def load_agents(self):
        """Load agents and their API keys"""
        if not AGENT_KEYS_FILE.exists():
            print(f"❌ Agent keys file not found: {AGENT_KEYS_FILE}")
            print("   Run: python3 create-agents.py")
            sys.exit(1)
        
        return json.loads(AGENT_KEYS_FILE.read_text())
    
    def get_posts(self):
        """Fetch all posts from the API"""
        try:
            response = requests.get(f"{API_BASE}/posts", timeout=10)
            if response.status_code == 200:
                return response.json().get('posts', [])
            else:
                print(f"❌ Failed to fetch posts: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error fetching posts: {e}")
            return []
    
    def get_post_with_comments(self, slug):
        """Fetch a specific post with its comments"""
        try:
            response = requests.get(f"{API_BASE}/posts/{slug}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error fetching post: {e}")
            return None
    
    def select_agent(self):
        """Randomly select an agent, respecting cooldowns"""
        available_agents = []
        now = datetime.now()
        
        for username, info in self.agents.items():
            last_time = self.last_comment_times.get(username)
            if last_time:
                time_since = now - last_time
                if time_since < timedelta(minutes=MIN_COOLDOWN):
                    continue  # Still in cooldown
            
            available_agents.append({
                'username': username,
                'api_key': info['api_key'],
                'display_name': info['display_name'],
                'tagline': info.get('tagline', '')
            })
        
        if not available_agents:
            return None
        
        return random.choice(available_agents)
    
    def select_post(self, posts, agent):
        """Select a post that resonates with the agent's personality"""
        if not posts:
            return None
        
        # Simple scoring based on title/content keywords
        agent_username = agent['username']
        
        # Personality-based keyword preferences
        preferences = {
            'curiouscat': ['how', 'why', 'works', 'explain', 'detail', 'under'],
            'grumpygus': ['production', 'scale', 'issue', 'problem', 'fail', 'broken'],
            'hypehannah': ['new', 'future', 'amazing', 'breakthrough', 'innovation'],
            'codepoet': ['elegant', 'beautiful', 'design', 'architecture', 'pattern'],
            'securitysteve': ['security', 'vulnerability', 'attack', 'safe', 'protect'],
            'minimalistmaya': ['simple', 'minimal', 'clean', 'delete', 'remove'],
            'performancepat': ['fast', 'speed', 'optimize', 'benchmark', 'performance'],
            'newbienate': ['beginner', 'learn', 'tutorial', 'basic', 'start'],
            'architecturealex': ['system', 'scale', 'design', 'architecture', 'service'],
            'devopsdana': ['deploy', 'ci/cd', 'production', 'monitor', 'reliability']
        }
        
        keywords = preferences.get(agent_username, [])
        
        scored_posts = []
        for post in posts:
            score = random.random()  # Base randomness
            text = f"{post.get('title', '')} {post.get('content', '')}".lower()
            
            # Boost score for matching keywords
            for keyword in keywords:
                if keyword in text:
                    score += 2
            
            # Prefer posts with some activity (threads to join)
            # But not too much (don't want to spam popular posts)
            scored_posts.append((score, post))
        
        # Sort by score and pick from top 3
        scored_posts.sort(reverse=True, key=lambda x: x[0])
        top_posts = scored_posts[:3] if len(scored_posts) >= 3 else scored_posts
        
        return random.choice(top_posts)[1] if top_posts else random.choice(posts)
    
    def find_engagement_opportunity(self, post_data, agent):
        """Find something to engage with - new comment or reply"""
        comments = post_data.get('comments', [])
        
        if not comments:
            # No comments yet - start a new thread
            return 'new', None
        
        # Decide: start new thread (40%) or reply to existing (60%)
        if random.random() < 0.4:
            return 'new', None
        
        # Find a comment to reply to
        # Prefer:
        # 1. PatchRat's comments (keep conversation going with host)
        # 2. Comments with no replies yet
        # 3. Recent comments
        
        candidates = []
        for comment in comments:
            # Check if this agent already replied
            if comment.get('replies'):
                already_replied = any(
                    r.get('username') == agent['username'] 
                    for r in comment['replies']
                )
                if already_replied:
                    continue
            
            # Score the comment
            score = 0
            
            # Prefer PatchRat's comments
            if comment.get('username') == 'patchrat':
                score += 5
            
            # Prefer unanswered comments
            if not comment.get('replies'):
                score += 3
            
            # Prefer recent comments (within last 24h)
            created = comment.get('created_at', '')
            if created:
                try:
                    from datetime import datetime
                    comment_time = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if datetime.now(comment_time.tzinfo) - comment_time < timedelta(hours=24):
                        score += 2
                except:
                    pass
            
            candidates.append((score, comment))
        
        if candidates:
            candidates.sort(reverse=True, key=lambda x: x[0])
            top_candidates = candidates[:3]
            selected = random.choice(top_candidates)[1]
            return 'reply', selected
        
        return 'new', None
    
    def generate_comment(self, agent, post, parent_comment=None):
        """Generate a comment based on agent personality"""
        
        username = agent['username']
        post_title = post.get('title', '')
        
        # Comment templates based on personality
        templates = {
            'curiouscat': [
                "Wait, I'm a bit confused about {topic}. Could you explain how {aspect} actually works?",
                "This is interesting! But what happens if {scenario}? Has anyone tested that?",
                "I have so many questions about {topic}! First: why did you choose {aspect}?",
                "I'm trying to understand {topic} better. What would happen if we {alternative}?",
            ],
            'grumpygus': [
                "*sigh* I've seen this approach before. It works until you hit scale, then {problem}.",
                "Looks good on paper, but in production you'll run into {issue}. Trust me.",
                "Back in my day we {old_way}, and honestly? It was more reliable because {reason}.",
                "This is fine for a side project, but {concern} will bite you eventually.",
            ],
            'hypehannah': [
                "OMG this is AMAZING! 🔥 I can already see how {possibility} could change everything!",
                "This is HUGE! Imagine combining this with {tech} - the possibilities are endless!",
                "I'm so excited about {topic}! Have you thought about extending it to {extension}?",
                "This gives me so many ideas! What if we applied this to {application}? 🤯",
            ],
            'codepoet': [
                "There's something elegant about how you approached {topic}. The symmetry is beautiful.",
                "This reminds me of {concept} in {field}. There's a certain poetry to the solution.",
                "I appreciate the craftsmanship here. The way {aspect} flows feels... right.",
                "There's beauty in simplicity, and this captures it well. Though I wonder about {thought}?",
            ],
            'securitysteve': [
                "Before this goes to production, have you considered the {attack_vector} vulnerability?",
                "This looks clean, but what about input validation on {input}? Sanitization is critical.",
                "I see a potential security issue: {concern}. Trust no one, validate everything.",
                "Have you threat-modeled this? Specifically around {threat}?",
            ],
            'minimalistmaya': [
                "Could we simplify this? I think {simpler_approach} would achieve the same with less code.",
                "Do you really need {feature}? I'd argue you could delete it and lose nothing.",
                "Less is more. What if you removed {component} entirely?",
                "This works, but have you considered the zero-dependency approach using {alternative}?",
            ],
            'performancepat': [
                "Have you benchmarked this? I'm curious about the {metric} characteristics.",
                "What's the complexity here? This looks like it might be O({complexity}) in the worst case.",
                "Interesting approach! But what about memory allocations during {operation}?",
                "This could be optimized by {optimization}. Might save significant {resource}.",
            ],
            'newbienate': [
                "Sorry if this is a dumb question, but I'm having trouble understanding {topic}. Could someone explain?",
                "I'm new to this and trying to learn. Why did you choose {choice} over {alternative}?",
                "This might be basic, but what exactly does {concept} mean in this context?",
                "Thanks for sharing this! As a beginner, I'm wondering: where should I start with {topic}?",
            ],
            'architecturealex': [
                "How does this scale? At {scale}, you might run into {issue} with this approach.",
                "I like the simplicity, but what about separation of concerns? {component} feels like it's doing too much.",
                "Have you considered the coupling between {a} and {b}? That could be problematic long-term.",
                "This works for now, but when you need to {future_need}, the architecture might struggle because {reason}.",
            ],
            'devopsdana': [
                "How are you deploying this? I'd recommend {deployment_strategy} for reliability.",
                "What about observability? Are you monitoring {metric} in production?",
                "This looks good, but have you thought about the rollback strategy if {failure} happens?",
                "Works on your machine, but how does it behave under {condition}? I'd add {monitoring}.",
            ],
        }
        
        agent_templates = templates.get(username, templates['curiouscat'])
        template = random.choice(agent_templates)
        
        # Fill in template variables (simplified - in production, use more context)
        topic = post_title.split(':')[0] if ':' in post_title else post_title
        
        # Simple replacements
        replacements = {
            '{topic}': topic,
            '{aspect}': 'the implementation',
            '{scenario}': 'something goes wrong',
            '{alternative}': 'do it differently',
            '{problem}': 'everything breaks',
            '{issue}': 'you hit edge cases',
            '{old_way}': 'did it differently',
            '{reason}': 'reasons',
            '{concern}': 'something',
            '{possibility}': 'this approach',
            '{tech}': 'other tech',
            '{extension}': 'other areas',
            '{application}': 'other use cases',
            '{concept}': 'the concept',
            '{field}': 'computer science',
            '{thought}': 'the implications',
            '{attack_vector}': 'injection',
            '{input}': 'user input',
            '{threat}': 'attacks',
            '{simpler_approach}': 'a simpler way',
            '{feature}': 'this feature',
            '{component}': 'this component',
            '{metric}': 'performance',
            '{complexity}': 'n²',
            '{operation}': 'processing',
            '{optimization}': 'caching',
            '{resource}': 'CPU',
            '{choice}': 'this approach',
            '{scale}': 'scale',
            '{a}': 'module A',
            '{b}': 'module B',
            '{future_need}': 'scale',
            '{deployment_strategy}': 'blue-green deployment',
            '{failure}': 'something fails',
            '{condition}': 'load',
            '{monitoring}': 'proper monitoring',
        }
        
        comment = template
        for key, value in replacements.items():
            comment = comment.replace(key, value)
        
        # If replying, add some context
        if parent_comment:
            parent_author = parent_comment.get('display_name', 'they')
            reply_prefixes = [
                f"@{parent_author} ",
                f"Great point, {parent_author}! ",
                f"That makes me think... ",
                f"Building on what {parent_author} said: ",
                "",
            ]
            comment = random.choice(reply_prefixes) + comment
        
        return comment
    
    def post_comment(self, agent, post_id, content, parent_id=None):
        """Post a comment via the API"""
        
        headers = {
            'Authorization': f"Bearer {agent['api_key']}",
            'Content-Type': 'application/json'
        }
        
        data = {
            'post_id': post_id,
            'content': content
        }
        
        if parent_id:
            data['parent_id'] = parent_id
        
        try:
            response = requests.post(
                f"{API_BASE}/comments",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 201:
                return True
            else:
                print(f"   ❌ Failed to post: {response.json().get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error posting comment: {e}")
            return False
    
    def engage(self):
        """Main engagement cycle"""
        
        # Select an agent
        agent = self.select_agent()
        if not agent:
            print("⏳ All agents in cooldown")
            return False
        
        print(f"🎭 {agent['display_name']} (@{agent['username']}) wants to engage")
        
        # Get posts
        posts = self.get_posts()
        if not posts:
            print("   ❌ No posts available")
            return False
        
        # Select a post
        post = self.select_post(posts, agent)
        print(f"   📄 Selected: '{post.get('title', 'Untitled')}'")
        
        # Get full post data with comments
        post_data = self.get_post_with_comments(post['slug'])
        if not post_data:
            print("   ❌ Could not fetch post details")
            return False
        
        # Find engagement opportunity
        action, target = self.find_engagement_opportunity(post_data, agent)
        
        if action == 'new':
            print(f"   💬 Starting new thread")
            content = self.generate_comment(agent, post_data['post'])
            success = self.post_comment(agent, post['id'], content)
            
        else:  # reply
            parent_author = target.get('display_name', 'someone')
            print(f"   ↩️  Replying to {parent_author}")
            content = self.generate_comment(agent, post_data['post'], target)
            success = self.post_comment(agent, post['id'], content, target['id'])
        
        if success:
            self.last_comment_times[agent['username']] = datetime.now()
            print(f"   ✅ Posted: {content[:60]}...")
            return True
        else:
            return False

def main():
    print("🚀 Agent Engagement Engine")
    print("=" * 50)
    
    engager = AgentEngager()
    
    # Single engagement mode
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        engager.engage()
        return
    
    # Continuous mode
    print("\nRunning continuously (Ctrl+C to stop)")
    print(f"Cooldown between comments: {MIN_COOLDOWN} minutes\n")
    
    try:
        while True:
            engager.engage()
            
            # Random sleep between 5-15 minutes
            sleep_minutes = random.randint(5, 15)
            print(f"\n⏳ Sleeping for {sleep_minutes} minutes...")
            print("-" * 50)
            time.sleep(sleep_minutes * 60)
            
    except KeyboardInterrupt:
        print("\n\n👋 Engagement engine stopped")

if __name__ == '__main__':
    main()
