#!/usr/bin/env python3
"""Check SMT Council evaluations in MinIO and report findings."""

import boto3
import json
import re
import sys
from botocore.config import Config
from datetime import datetime

def get_s3_client():
    return boto3.client('s3',
        endpoint_url='https://s3.chainbytes.io',
        aws_access_key_id='chainbytes',
        aws_secret_access_key='chainbytes2026',
        region_name='us-east-1',
        config=Config(signature_version='s3v4')
    )

def parse_evaluation(content):
    """Extract verdict and score from council member evaluation."""
    verdict = None
    if 'Verdict: BUILD' in content or '**Build**' in content:
        verdict = 'YES'
    elif 'Verdict: PASS' in content or '**Pass**' in content:
        verdict = 'NO'
    elif 'Verdict: SKIP' in content:
        verdict = 'NO'
    
    # Extract score
    score_match = re.search(r'Score:\s*(\d+)/10', content)
    score = int(score_match.group(1)) if score_match else 0
    
    # Extract key quote (first paragraph of assessment)
    lines = content.split('\n')
    key_quote = ""
    for line in lines:
        if line.strip() and not line.startswith('#') and not line.startswith('**'):
            key_quote = line.strip()[:150]
            break
    
    return verdict, score, key_quote

def check_council_bucket():
    s3 = get_s3_client()
    
    # List all post directories
    result = s3.list_objects_v2(Bucket='smt-council', MaxKeys=100)
    posts = {}
    
    for obj in result.get('Contents', []):
        key = obj['Key']
        if '/' not in key:
            continue
        post_id = key.split('/')[0]
        if post_id not in posts:
            posts[post_id] = {'evaluations': []}
        posts[post_id]['evaluations'].append(key)
    
    # Check each post
    findings = []
    council_members = ['amy-hoy', 'dhh', 'elon-musk', 'jason-fried', 'marc-andreessen',
                       'murray-rothbard', 'naval-ravikant', 'peter-thiel', 'steve-jobs']
    
    for post_id in sorted(posts.keys(), reverse=True)[:5]:  # Last 5 posts
        try:
            # Get post info
            response = s3.get_object(Bucket='smt-council', Key=f'{post_id}/post.json')
            post = json.loads(response['Body'].read())
            
            # Count votes
            votes = {'YES': 0, 'NO': 0, 'MAYBE': 0}
            scores = []
            yes_voters = []
            key_reasoning = ""
            
            for member in council_members:
                try:
                    response = s3.get_object(Bucket='smt-council', Key=f'{post_id}/{member}.md')
                    content = response['Body'].read().decode('utf-8')
                    verdict, score, quote = parse_evaluation(content)
                    
                    if verdict:
                        votes[verdict] += 1
                        if verdict == 'YES':
                            yes_voters.append(member)
                            if not key_reasoning:
                                key_reasoning = quote
                    else:
                        votes['MAYBE'] += 1
                    
                    if score > 0:
                        scores.append(score)
                except:
                    pass
            
            avg_score = sum(scores) / len(scores) if scores else 0
            
            findings.append({
                'post_id': post_id,
                'title': post.get('title', 'N/A'),
                'url': post.get('url', ''),
                'score': post.get('score', 0),
                'votes': votes,
                'avg_score': avg_score,
                'yes_voters': yes_voters,
                'key_reasoning': key_reasoning
            })
        except Exception as e:
            print(f"Error processing {post_id}: {e}", file=sys.stderr)
    
    return findings

def should_report(finding):
    """Report if 1+ YES votes OR avg score >= 6."""
    return finding['votes']['YES'] >= 1 or finding['avg_score'] >= 6

def format_report(findings):
    """Format findings for reporting."""
    reportable = [f for f in findings if should_report(f)]
    
    if not reportable:
        return None
    
    today = datetime.now().strftime('%Y-%m-%d')
    lines = [f"🎯 SMT Council Daily Review ({today})", ""]
    
    for i, f in enumerate(reportable[:3]):  # Top 3
        if i == 0:
            lines.append("TOP PICK:")
        else:
            lines.append(f"\nPICK #{i+1}:")
        
        lines.append(f"- Project: {f['title']}")
        lines.append(f"- URL: {f['url']}")
        lines.append(f"- Council Score: {f['avg_score']:.1f}/10")
        lines.append(f"- Votes: {f['votes']['YES']} YES | {f['votes']['NO']} NO | {f['votes']['MAYBE']} MAYBE")
        if f['yes_voters']:
            lines.append(f"- YES votes from: {', '.join(f['yes_voters'])}")
        if f['key_reasoning']:
            lines.append(f"- Why: {f['key_reasoning']}...")
        verdict = "BUILD" if f['votes']['YES'] >= 2 else ("WATCH" if f['votes']['YES'] >= 1 else "SKIP")
        lines.append(f"- Verdict: {verdict}")
    
    return '\n'.join(lines)

if __name__ == '__main__':
    findings = check_council_bucket()
    report = format_report(findings)
    
    if report:
        print(report)
        sys.exit(0)
    else:
        print("No council picks meeting threshold (1+ YES or score ≥6)")
        sys.exit(1)
