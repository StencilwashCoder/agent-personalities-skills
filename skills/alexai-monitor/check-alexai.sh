#!/bin/bash
# AlexAI Facebook Monitor - Check existing Apify runs for GitHub repos
# Usage: ./check-alexai.sh

set -e

APIFY_TOKEN="${APIFY_TOKEN:-your_apify_token_here}"
BOT_TOKEN="8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
CHAT_ID="84020120"
WORKSPACE_DIR="/root/.openclaw/workspace"
REPO_FILE="$WORKSPACE_DIR/memory/alexai-repos.json"
LAST_CHECK_FILE="$WORKSPACE_DIR/memory/alexai-last-check.json"

# Send Telegram message
send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=$message" \
        -d "parse_mode=HTML" > /dev/null
}

# Check if we should run (skip if checked within 6 hours)
should_run() {
    if [ -f "$LAST_CHECK_FILE" ]; then
        local last_check=$(jq -r '.lastCheck // empty' "$LAST_CHECK_FILE")
        if [ -n "$last_check" ]; then
            local last_epoch=$(date -d "$last_check" +%s 2>/dev/null || echo 0)
            local now=$(date +%s)
            local diff=$((now - last_epoch))
            if [ $diff -lt 21600 ]; then  # 6 hours
                echo "⏭️ Skipped: Last check was $((diff / 60)) minutes ago"
                exit 0
            fi
        fi
    fi
}

# Get recent runs for Facebook scraper
get_recent_runs() {
    curl -s "https://api.apify.com/v2/acts/scrapio~facebook-page-scraper/runs?token=$APIFY_TOKEN&status=SUCCEEDED&limit=5" | \
        jq -r '.data.items[].id'
}

# Get dataset items from a run
get_dataset_items() {
    local run_id="$1"
    curl -s "https://api.apify.com/v2/actor-runs/$run_id/dataset/items?token=$APIFY_TOKEN" | \
        jq -r '.[] | @base64'
}

# Extract GitHub repos from post/comment text
extract_repos() {
    local text="$1"
    echo "$text" | grep -oE 'https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+' | sort -u
}

# Main check function
check_runs() {
    local new_repos="[]"
    local existing_repos=$(jq -r '.repos[].url // empty' "$REPO_FILE" 2>/dev/null || echo "")
    
    echo "🔍 Checking recent Apify runs..."
    
    for run_id in $(get_recent_runs); do
        echo "  Checking run: $run_id"
        
        get_dataset_items "$run_id" | while read -r encoded; do
            local item=$(echo "$encoded" | base64 -d)
            local post_text=$(echo "$item" | jq -r '.text // .postText // empty')
            local comments=$(echo "$item" | jq -r '.comments[].text // empty' 2>/dev/null || echo "")
            
            # Check post text
            for repo_url in $(extract_repos "$post_text"); do
                if ! echo "$existing_repos" | grep -q "$repo_url"; then
                    local repo_name=$(echo "$repo_url" | sed 's|https://github.com/||')
                    echo "Found new repo: $repo_name"
                    new_repos=$(echo "$new_repos" | jq --arg url "$repo_url" --arg name "$repo_name" '. += [{url: $url, name: $name, date: "'$(date -I)'", isNew: true}]')
                fi
            done
            
            # Check comments
            for comment in $comments; do
                for repo_url in $(extract_repos "$comment"); do
                    if ! echo "$existing_repos" | grep -q "$repo_url"; then
                        local repo_name=$(echo "$repo_url" | sed 's|https://github.com/||')
                        echo "Found new repo in comment: $repo_name"
                        new_repos=$(echo "$new_repos" | jq --arg url "$repo_url" --arg name "$repo_name" '. += [{url: $url, name: $name, date: "'$(date -I)'", isNew: true}]')
                    fi
                done
            done
        done
    done
    
    echo "$new_repos"
}

# Main
main() {
    should_run
    
    # Check runs and get new repos
    local new_repos=$(check_runs)
    
    # Update last check time
    jq -n --arg date "$(date -Iseconds)" '{lastCheck: $date}' > "$LAST_CHECK_FILE"
    
    # If new repos found, update file and send digest
    if [ "$(echo "$new_repos" | jq length)" -gt 0 ]; then
        # Add to stored repos
        local all_repos=$(jq --argjson new "$new_repos" '.repos += $new' "$REPO_FILE")
        echo "$all_repos" > "$REPO_FILE"
        
        # Send Telegram digest
        local date_str=$(date +%Y-%m-%d)
        local message="📊 <b>AlexAI Daily Repo Digest ($date_str)</b>\n\n"
        message+="Found $(echo "$new_repos" | jq length) new GitHub repositories:\n\n"
        
        local count=1
        echo "$new_repos" | jq -c '.[]' | while read -r repo; do
            local name=$(echo "$repo" | jq -r '.name')
            local url=$(echo "$repo" | jq -r '.url')
            message+="$count. <b>$name</b>\n"
            message+="   🔗 $url\n\n"
            count=$((count + 1))
        done
        
        send_telegram "$message"
        echo "✅ Sent digest with $(echo "$new_repos" | jq length) new repos"
    else
        echo "📭 No new repos found today"
    fi
}

main "$@"
