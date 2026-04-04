#!/usr/bin/env python3
"""
Facebook Comments Scraper for AlexAI
Extracts GitHub links from Facebook post comments
"""

import asyncio
import json
import re
import sys
from playwright.async_api import async_playwright

FACEBOOK_PAGE = "https://www.facebook.com/Alexaiupdate"
GITHUB_PATTERN = re.compile(r'https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+')

async def scrape_facebook_comments():
    """Scrape comments from AlexAI Facebook page"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        try:
            # Navigate to page
            await page.goto(FACEBOOK_PAGE, timeout=60000)
            await page.wait_for_load_state('networkidle')
            
            # Wait for posts to load
            await page.wait_for_selector('[role="article"]', timeout=30000)
            
            # Find all comment links
            comment_links = await page.query_selector_all('a[href*="comment"], a[href*="/posts/"]')
            
            github_links = []
            
            # Click on each comment section to expand
            for i, link in enumerate(comment_links[:5]):  # Limit to first 5 posts
                try:
                    await link.click()
                    await asyncio.sleep(2)
                    
                    # Get page content
                    content = await page.content()
                    matches = GITHUB_PATTERN.findall(content)
                    github_links.extend(matches)
                    
                except Exception as e:
                    print(f"Error on post {i}: {e}", file=sys.stderr)
                    continue
            
            # Deduplicate
            unique_links = list(set(github_links))
            
            result = {
                "source": FACEBOOK_PAGE,
                "total_posts_checked": len(comment_links[:5]),
                "github_links_found": len(unique_links),
                "repos": unique_links
            }
            
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_facebook_comments())
