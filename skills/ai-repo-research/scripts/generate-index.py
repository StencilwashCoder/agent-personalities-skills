import json
import os
import sys

def generate_index(repo_count, total_stars, output_path):
    # Load repos from JSON file
    repos_json_path = os.path.join(os.path.dirname(output_path), 'repos.json')
    repos_data = []
    if os.path.exists(repos_json_path):
        with open(repos_json_path, 'r') as f:
            repos_data = json.load(f)
    
    repos_js = json.dumps(repos_data)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Repo Research</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <div>
      <h1>🤖 AI Repo Research</h1>
      <p>Curated research on AI-related GitHub repositories</p>
    </div>
    <div class="stats">
      <div class="stat">
        <div class="stat-value">{repo_count}</div>
        <div class="stat-label">Repos</div>
      </div>
      <div class="stat">
        <div class="stat-value">{total_stars}</div>
        <div class="stat-label">Stars</div>
      </div>
    </div>
  </header>

  <div class="controls">
    <input type="text" id="search" placeholder="🔍 Search repos, topics..." oninput="renderRepos()">
    <select id="sort" onchange="renderRepos()">
      <option value="stars-desc">⭐ Most Stars</option>
      <option value="stars-asc">⭐ Least Stars</option>
      <option value="name-asc">A-Z Name</option>
      <option value="name-desc">Z-A Name</option>
      <option value="newest">📅 Newest</option>
      <option value="oldest">📅 Oldest</option>
    </select>
    <select id="filter-lang" onchange="renderRepos()">
      <option value="">All Languages</option>
    </select>
  </div>

  <div class="repo-grid" id="repo-grid">
    <!-- Repos will be rendered by JavaScript -->
  </div>

  <footer>
    <p>Generated • <a href="https://github.com">Data from GitHub</a></p>
  </footer>

  <script>
    const repos = {repos_js};
    
    function populateLanguages() {{
      const langs = [...new Set(repos.map(r => r.language).filter(Boolean))].sort();
      const select = document.getElementById('filter-lang');
      langs.forEach(lang => {{
        const opt = document.createElement('option');
        opt.value = lang;
        opt.textContent = lang;
        select.appendChild(opt);
      }});
    }}
    
    function renderRepos() {{
      const search = document.getElementById('search').value.toLowerCase();
      const sort = document.getElementById('sort').value;
      const langFilter = document.getElementById('filter-lang').value;
      const grid = document.getElementById('repo-grid');
      
      let filtered = repos.filter(repo => {{
        const matchesSearch = repo.name.toLowerCase().includes(search) || 
                             repo.description.toLowerCase().includes(search) ||
                             (repo.topics && repo.topics.toLowerCase().includes(search));
        const matchesLang = !langFilter || repo.language === langFilter;
        return matchesSearch && matchesLang;
      }});
      
      filtered.sort((a, b) => {{
        switch(sort) {{
          case 'stars-desc': return b.stars - a.stars;
          case 'stars-asc': return a.stars - b.stars;
          case 'name-asc': return a.name.localeCompare(b.name);
          case 'name-desc': return b.name.localeCompare(a.name);
          case 'newest': return (b.created || '').localeCompare(a.created || '');
          case 'oldest': return (a.created || '').localeCompare(b.created || '');
          default: return 0;
        }}
      }});
      
      if (filtered.length === 0) {{
        grid.innerHTML = '<div class="no-results">No repos match your search</div>';
        return;
      }}
      
      grid.innerHTML = filtered.map(repo => {{
        const topics = repo.topics ? repo.topics.split(',').slice(0, 3) : [];
        return '<div class="repo-card" onclick="window.location=\\'repos/' + repo.safeName + '.html\\'">' +
          '<div class="repo-header">' +
            '<a href="repos/' + repo.safeName + '.html" class="repo-name" onclick="event.stopPropagation()">' + repo.name + '</a>' +
            '<div class="repo-badges">' +
              '<span class="badge badge-stars">⭐ ' + repo.stars.toLocaleString() + '</span>' +
              '<span class="badge badge-lang">' + (repo.language || '?') + '</span>' +
            '</div>' +
          '</div>' +
          '<div class="repo-desc">' + (repo.description || 'No description') + '</div>' +
          '<div class="repo-meta">' +
            topics.map(t => '<span class="topic-tag">' + t + '</span>').join('') +
          '</div>' +
        '</div>';
      }}).join('');
    }}
    
    // Initialize
    populateLanguages();
    renderRepos();
  </script>
</body>
</html>'''
    
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"Generated: {output_path}")

if __name__ == '__main__':
    repo_count = sys.argv[1] if len(sys.argv) > 1 else '0'
    total_stars = sys.argv[2] if len(sys.argv) > 2 else '0'
    output_path = sys.argv[3] if len(sys.argv) > 3 else 'index.html'
    generate_index(repo_count, total_stars, output_path)
