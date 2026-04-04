import { config } from 'dotenv';
import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';

config();

function validateEnv() {
  const required = ['GITHUB_USERNAME', 'WEBSITE_URL'];
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    throw new Error(`Missing required env vars: ${missing.join(', ')}`);
  }
}

function generateOptimizedProfile(userData) {
  const website = process.env.WEBSITE_URL || 'https://ericgrill.com';
  const tagline = process.env.WEBSITE_TAGLINE || 'Building innovative software solutions';
  const bio = process.env.BIO_LONG || 'Full-stack developer and entrepreneur';
  const twitter = process.env.PERSONAL_TWITTER || '@ericgrill';
  
  return `<!-- 
  Optimized GitHub Profile for SEO
  Generated for: ${userData.login}
  Website: ${website}
-->

<h1 align="center">Hi, I'm ${userData.name || 'Eric'} 👋</h1>

<p align="center">
  <strong>${tagline}</strong>
</p>

<p align="center">
  <a href="${website}">🌐 Website</a> •
  <a href="https://twitter.com/${twitter.replace('@', '')}">🐦 Twitter</a> •
  <a href="https://linkedin.com/in/${process.env.GITHUB_USERNAME}">💼 LinkedIn</a>
</p>

---

## 🚀 About Me

${bio}

- 🔭 Currently working on **[${website.replace('https://', '')}](${website})**
- 🌱 Learning: Blockchain, AI/ML, Cloud Architecture
- 👯 Looking to collaborate on: Open source projects
- 💬 Ask me about: Full-stack development, Startups, System design
- 📫 Reach me: [${website}](${website})

## 🛠️ Tech Stack

![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/-React-61DAFB?style=flat&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/-Node.js-339933?style=flat&logo=node.js&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=${userData.login}&show_icons=true&theme=dark" alt="GitHub Stats" />
</p>

## 🔗 Quick Links

- 🌐 **Website:** [${website}](${website})
- 📝 **Blog:** [${website}/blog](${website}/blog)
- 💼 **Portfolio:** [${website}/projects](${website}/projects)
- 📧 **Contact:** [${website}/contact](${website}/contact)

---

<p align="center">
  💻 Building the future, one commit at a time.
</p>
`;
}

export async function optimizeGitHub() {
  validateEnv();
  
  const username = process.env.GITHUB_USERNAME;
  const token = process.env.GITHUB_TOKEN;
  const outputDir = './output/github';
  
  await fs.ensureDir(outputDir);
  
  let userData = {
    login: username,
    name: process.env.PERSONAL_NAME || 'Eric Grill',
    bio: process.env.BIO_SHORT || 'Software Engineer',
    blog: process.env.WEBSITE_URL
  };
  
  // If token provided, fetch real data
  if (token) {
    try {
      const { Octokit } = await import('@octokit/rest');
      const octokit = new Octokit({ auth: token });
      
      const { data } = await octokit.rest.users.getAuthenticated();
      userData = data;
      
      // Check if website is set
      const analysis = {
        username: data.login,
        name: data.name,
        currentBlog: data.blog,
        currentBio: data.bio,
        websiteInBio: data.bio?.includes('ericgrill.com'),
        websiteInBlog: data.blog?.includes('ericgrill.com'),
        hireable: data.hireable,
        publicRepos: data.public_repos,
        followers: data.followers,
        recommendations: []
      };
      
      if (!data.blog || !data.blog.includes('ericgrill.com')) {
        analysis.recommendations.push('⚠️  Website URL not set or incorrect in profile');
      }
      
      if (!data.bio || data.bio.length < 50) {
        analysis.recommendations.push('⚠️  Bio is too short for optimal SEO');
      }
      
      await fs.writeJson(path.join(outputDir, 'seo-analysis.json'), analysis, { spaces: 2 });
      
    } catch (error) {
      console.log(chalk.yellow(`   ⚠️  Could not fetch GitHub data: ${error.message}`));
      console.log(chalk.yellow('   Continuing with template generation...'));
    }
  }
  
  // Generate optimized profile README
  const optimizedProfile = generateOptimizedProfile(userData);
  await fs.writeFile(path.join(outputDir, 'profile-optimized.md'), optimizedProfile);
  
  // Generate GitHub Actions workflow for profile README
  const workflowContent = `name: Generate Profile README

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update README
        run: |
          # Add any dynamic content generation here
          echo "Last updated: $(date)" >> README.md
      - name: Commit changes
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add README.md
          git diff --quiet && git diff --staged --quiet || git commit -m "Update profile"
          git push
`;
  
  await fs.ensureDir(path.join(outputDir, '.github', 'workflows'));
  await fs.writeFile(
    path.join(outputDir, '.github', 'workflows', 'profile-readme.yml'),
    workflowContent
  );
  
  // Generate setup instructions
  const instructions = `# GitHub Profile SEO Optimization

## Current Status
- Username: ${userData.login}
- Name: ${userData.name}
- Blog URL: ${userData.blog || 'NOT SET'}

## Quick Setup

### 1. Create Profile Repository
\`\`\`bash
# Create a repository named exactly as your username
# This creates a special profile README
\`\`\`

### 2. Copy Optimized Profile
Copy \`profile-optimized.md\` to your profile repo as \`README.md\`

### 3. Update Profile Settings
Go to https://github.com/settings/profile and set:
- **Name:** ${process.env.PERSONAL_NAME || 'Eric Grill'}
- **Public email:** (your email)
- **Bio:** ${process.env.BIO_SHORT || 'Software engineer building the future'}
- **URL:** ${process.env.WEBSITE_URL || 'https://ericgrill.com'}
- **Twitter username:** ${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}
- **Company:** Your company or "Independent"
- **Location:** Your location

### 4. Enable Profile README
Create a public repository named exactly: \`${username}\`
Add the optimized README.md to this repo.

### 5. Pin Important Repositories
Pin repositories that:
- Link to ericgrill.com in their README
- Are actively maintained
- Showcase your best work
- Have good documentation

## SEO Checklist

- [ ] Profile repository created (\`${username}/${username}\`)
- [ ] Website URL set in profile
- [ ] Bio includes relevant keywords
- [ ] README includes backlinks to ericgrill.com
- [ ] Pinned repositories link to website
- [ ] Twitter link included
- [ ] LinkedIn link included

## Profile Repository Structure

\`\`\`
${username}/
├── README.md              # Your profile (use profile-optimized.md)
├── .github/
│   └── workflows/
│       └── profile-readme.yml  # Auto-update workflow
└── assets/
    └── banner.png         # Optional custom banner
\`\`\`
`;
  
  await fs.writeFile(path.join(outputDir, 'SETUP.md'), instructions);
  
  return {
    status: 'success',
    automated: !!token,
    username,
    outputs: [
      'output/github/profile-optimized.md',
      'output/github/seo-analysis.json',
      'output/github/SETUP.md',
      'output/github/.github/workflows/profile-readme.yml'
    ]
  };
}
