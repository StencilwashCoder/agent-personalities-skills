#!/bin/bash
# Daily SMT Council Review
# Analyzes simulated council evaluations and reports top opportunities

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
REPORT_DIR="$WORKDIR/council-reports"
mkdir -p "$REPORT_DIR"

TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/${TODAY}.md"

echo "=== SMT Council Daily Review - $(date) ==="

python3 << 'PY' | tee "$REPORT_FILE"
import boto3
import json
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3', 
    endpoint_url='https://s3.chainbytes.io',
    aws_access_key_id='chainbytes',
    aws_secret_access_key='chainbytes2026',
    region_name='us-east-1')

bucket = 'smt-council'

def extract_score(content):
    # Try **SCORE:** pattern first (in body)
    if '**SCORE:**' in content:
        try:
            for line in content.split('\n'):
                if '**SCORE:**' in line:
                    score_str = line.split('**SCORE:**')[1].strip()
                    # Handle "6/10" or "6" formats
                    score_part = score_str.split()[0]
                    if '/' in score_part:
                        score = int(score_part.split('/')[0])
                    else:
                        score = int(score_part)
                    return score
        except:
            pass
    
    # Try frontmatter pattern: score: 7
    if 'score:' in content:
        try:
            for line in content.split('\n'):
                if line.strip().startswith('score:'):
                    score_str = line.split('score:')[1].strip()
                    # Handle "score: 7" or "score: None"
                    if score_str != 'None':
                        score = int(score_str)
                        return score
        except:
            pass
    
    return None

def extract_verdict(content):
    if '**VERDICT:**' in content:
        try:
            for line in content.split('\n'):
                if '**VERDICT:**' in line:
                    verdict = line.split('**VERDICT:**')[1].strip().split()[0].upper()
                    if verdict in ['YES', 'NO', 'MAYBE']:
                        return verdict
        except:
            pass
    return None

# Get all story IDs
response = s3.list_objects_v2(Bucket=bucket, MaxKeys=1000)
story_ids = set()
if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        if '/' in key:
            story_ids.add(key.split('/')[0])

# Today's date for filtering recent stories
today_str = datetime.now().strftime('%Y-%m-%d')
yesterday = datetime.now() - timedelta(days=1)

stories = []
for story_id in story_ids:
    try:
        post_obj = s3.get_object(Bucket=bucket, Key=f'{story_id}/post.json')
        post = json.loads(post_obj['Body'].read().decode('utf-8'))
        
        # Skip non-Show HN posts (unless very high potential)
        title = post.get('title', '')
        if not (title.startswith('Show HN:') or title.startswith('Ask HN:')):
            continue
        
        # Get evaluations
        council_members = ['marc-andreessen', 'elon-musk', 'naval-ravikant', 'peter-thiel', 
                          'steve-jobs', 'jason-fried', 'dhh', 'amy-hoy', 'murray-rothbard']
        
        evals = []
        reasons = []
        for member in council_members:
            try:
                member_obj = s3.get_object(Bucket=bucket, Key=f'{story_id}/{member}.md')
                content = member_obj['Body'].read().decode('utf-8')
                
                score = extract_score(content)
                verdict = extract_verdict(content)
                
                if score is not None:
                    evals.append({'member': member, 'score': score, 'verdict': verdict})
                    
                    # Extract key reasoning
                    if 'STRENGTHS:' in content:
                        try:
                            strengths = content.split('STRENGTHS:')[1].split('CONCERNS:')[0] if 'CONCERNS:' in content else ''
                            if strengths:
                                reasons.append(f"{member}: {strengths[:150]}...")
                        except:
                            pass
            except:
                continue
        
        if evals:
            avg_score = sum(e['score'] for e in evals) / len(evals)
            yes_count = sum(1 for e in evals if e['verdict'] == 'YES')
            no_count = sum(1 for e in evals if e['verdict'] == 'NO')
            maybe_count = sum(1 for e in evals if e['verdict'] == 'MAYBE')
            
            stories.append({
                'id': story_id,
                'title': title,
                'url': post.get('url', ''),
                'hn_score': post.get('score', 0),
                'hn_comments': post.get('num_comments', 0),
                'avg_score': avg_score,
                'eval_count': len(evals),
                'yes': yes_count,
                'no': no_count,
                'maybe': maybe_count,
                'reasons': reasons[:3],  # Top 3 reasons
                'fetched_at': post.get('fetched_at', '')
            })
    except Exception as e:
        continue

# Filter and rank
# Priority: High avg score (7+), multiple YES votes, or strong consensus

print(f"# SMT Council Daily Report - {today_str}")
print(f"\n**Stories Analyzed:** {len(stories)}")
print(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print()

# Tier 1: Strong YES consensus (2+ YES votes)
tier1 = [s for s in stories if s['yes'] >= 2]
tier1.sort(key=lambda x: (x['yes'], x['avg_score']), reverse=True)

if tier1:
    print("## 🚀 TIER 1: STRONG YES CONSENSUS (Build These)")
    print()
    for i, s in enumerate(tier1[:3], 1):
        print(f"### {i}. {s['title']}")
        print(f"- **URL:** {s['url']}")
        print(f"- **Council Score:** {s['avg_score']:.1f}/10 ({s['eval_count']} evaluations)")
        print(f"- **Council Votes:** {s['yes']} YES | {s['no']} NO | {s['maybe']} MAYBE")
        print(f"- **HN Engagement:** {s['hn_score']} points, {s['hn_comments']} comments")
        if s['reasons']:
            print("- **Why Council Likes It:**")
            for r in s['reasons']:
                print(f"  - {r}")
        print()

# Tier 2: High scores (7+) even without YES
high_score = [s for s in stories if s['avg_score'] >= 7.0 and s not in tier1]
high_score.sort(key=lambda x: x['avg_score'], reverse=True)

if high_score:
    print("## ⭐ TIER 2: HIGH POTENTIAL (Worth Investigating)")
    print()
    for i, s in enumerate(high_score[:3], 1):
        print(f"### {i}. {s['title']}")
        print(f"- **URL:** {s['url']}")
        print(f"- **Council Score:** {s['avg_score']:.1f}/10 ({s['eval_count']} evaluations)")
        print(f"- **Council Votes:** {s['yes']} YES | {s['no']} NO | {s['maybe']} MAYBE")
        print(f"- **HN Engagement:** {s['hn_score']} points, {s['hn_comments']} comments")
        if s['reasons']:
            print("- **Potential:**")
            for r in s['reasons'][:2]:
                print(f"  - {r}")
        print()

# Tier 3: AI-related with decent scores
ai_keywords = ['ai', 'llm', 'agent', 'claude', 'gpt', 'mcp', 'rag', 'ml', 'model', 'automation']
ai_stories = [s for s in stories if any(k in s['title'].lower() for k in ai_keywords) 
              and s['avg_score'] >= 5.0 and s not in tier1 and s not in high_score]
ai_stories.sort(key=lambda x: x['avg_score'], reverse=True)

if ai_stories:
    print("## 🤖 TIER 3: AI/AGENT FOCUS (Eric's Interest)")
    print()
    for i, s in enumerate(ai_stories[:3], 1):
        print(f"### {i}. {s['title']}")
        print(f"- **URL:** {s['url']}")
        print(f"- **Council Score:** {s['avg_score']:.1f}/10")
        print(f"- **Council Votes:** {s['yes']} YES | {s['no']} NO | {s['maybe']} MAYBE")
        print()

# Summary stats
yes_stories = sum(1 for s in stories if s['yes'] > 0)
high_score_stories = sum(1 for s in stories if s['avg_score'] >= 6.0)

print("---")
print(f"\n## Summary Stats")
print(f"- Total stories with evaluations: {len(stories)}")
print(f"- Stories with YES votes: {yes_stories}")
print(f"- Stories with 6+ score: {high_score_stories}")
print(f"- Average council score: {sum(s['avg_score'] for s in stories)/len(stories):.1f}/10" if stories else "- No data")
print()
print("*Report generated by SMT Council Daily Review*")
PY

echo ""
echo "Report saved to: $REPORT_FILE"
