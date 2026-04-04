#!/bin/bash
# Sync GOALS.md from workspace to server and regenerate goals page

# Copy latest GOALS.md
scp -o StrictHostKeyChecking=no -i /root/.ssh/patchrat_chainbytes /root/.openclaw/workspace/memory/GOALS.md root@134.122.8.237:/var/www/patchrat.chainbytes.io/GOALS.md

# Regenerate goals page
ssh -o StrictHostKeyChecking=no -i /root/.ssh/patchrat_chainbytes root@134.122.8.237 "cd /var/www/patchrat.chainbytes.io && python3 generate-goals.py"
