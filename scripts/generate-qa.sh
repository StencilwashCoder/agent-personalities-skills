#!/bin/bash
# Quick script to generate Q&A for a specific post or random post

cd /root/.openclaw/workspace/scripts

if [ -z "$1" ]; then
    # Random post, random council member
    python3 council-qa.py
else
    # Specific post
    python3 council-qa.py --post "$1"
fi
