#!/bin/bash
# List available Gemini models

echo "🔍 Checking available Gemini models..."

API_KEY="${GEMINI_API_KEY:-${GOOGLE_API_KEY:-$(cat ~/.gemini_key 2>/dev/null || cat ~/.google_api_key 2>/dev/null)}}"

if [ -z "$API_KEY" ]; then
    echo "❌ No API key found"
    exit 1
fi

curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$API_KEY" | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Available models:')
for m in data.get('models', []):
    name = m['name'].replace('models/', '')
    supported = ', '.join(m.get('supportedGenerationMethods', []))
    if 'generateContent' in supported:
        print(f'  ✅ {name}')
    else:
        print(f'  ⏭️  {name} (text only)')
"
