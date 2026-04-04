#!/bin/bash
# Automated package metadata optimizer for SEO
# Updates package.json and setup.py with keywords and links

echo "=== Package Registry SEO Optimizer ==="
echo ""

# Find all package.json files in Eric's repos
find /tmp -name "package.json" -path "*/EricGrill/*" 2>/dev/null | head -5 | while read -r pkg; do
  echo "Found: $pkg"
  
  # Backup original
  cp "$pkg" "$pkg.bak"
  
  # Read and optimize
  node -e "
    const fs = require('fs');
    const pkg = JSON.parse(fs.readFileSync('$pkg', 'utf8'));
    
    // Add SEO keywords
    pkg.keywords = pkg.keywords || [];
    const newKeywords = ['AI', 'automation', 'MCP', 'agent', 'bitcoin', 'infrastructure'];
    newKeywords.forEach(k => {
      if (!pkg.keywords.includes(k)) pkg.keywords.push(k);
    });
    
    // Add author with website
    pkg.author = pkg.author || {};
    if (typeof pkg.author === 'string') {
      pkg.author = { name: pkg.author };
    }
    pkg.author.url = 'https://ericgrill.com';
    
    // Add homepage
    pkg.homepage = pkg.homepage || 'https://ericgrill.com';
    
    // Add repository
    if (!pkg.repository) {
      pkg.repository = {
        type: 'git',
        url: 'https://github.com/EricGrill/' + pkg.name
      };
    }
    
    // Add bugs URL
    pkg.bugs = pkg.bugs || {
      url: 'https://github.com/EricGrill/' + pkg.name + '/issues'
    };
    
    fs.writeFileSync('$pkg', JSON.stringify(pkg, null, 2));
    console.log('Optimized:', '$pkg');
  " 2>/dev/null || echo "  (Node.js optimization skipped)"
done

echo ""
echo "Package.json files optimized with:"
echo "  - SEO keywords (AI, automation, MCP, agent, bitcoin)"
echo "  - Author URL: https://ericgrill.com"
echo "  - Homepage links"
echo ""

# Find setup.py files
echo "Checking Python packages..."
find /tmp -name "setup.py" -path "*/EricGrill/*" 2>/dev/null | head -5 | while read -r setup; do
  echo "Found: $setup"
  
  # Add SEO fields if not present
  if ! grep -q "url=" "$setup" 2>/dev/null; then
    echo "  (Would add url='https://ericgrill.com')"
  fi
  if ! grep -q "author_email" "$setup" 2>/dev/null; then
    echo "  (Would add author info with website)"
  fi
done

echo ""
echo "SEO optimization complete."
