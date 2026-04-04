import { config } from 'dotenv';
import axios from 'axios';
import fs from 'fs-extra';
import path from 'path';

config();

const HASHNODE_API = 'https://gql.hashnode.com';

export async function optimizeHashnode() {
  const token = process.env.HASHNODE_TOKEN;
  const username = process.env.HASHNODE_USERNAME || 'ericgrill';
  const outputDir = './output/hashnode';
  
  await fs.ensureDir(outputDir);
  
  const profileSettings = {
    name: process.env.PERSONAL_NAME || 'Eric Grill',
    tagline: process.env.BIO_SHORT || 'Software engineer building the future',
    website: process.env.WEBSITE_URL || 'https://ericgrill.com',
    bio: process.env.BIO_LONG || 'Full-stack developer and entrepreneur',
    location: '',
    social: {
      twitter: process.env.PERSONAL_TWITTER || '@ericgrill',
      github: process.env.GITHUB_USERNAME || 'ericgrill',
      linkedin: process.env.PERSONAL_LINKEDIN || '',
      website: process.env.WEBSITE_URL || 'https://ericgrill.com'
    },
    seo: {
      title: `${process.env.PERSONAL_NAME || 'Eric Grill'} - Software Engineer`,
      description: process.env.WEBSITE_DESCRIPTION || 'Personal website and portfolio',
      keywords: (process.env.KEYWORDS || 'software,engineering,startup').split(',')
    }
  };
  
  // Generate profile optimization guide
  const profileGuide = `# Hashnode Profile Optimization Guide

## Profile Settings

Visit: https://hashnode.com/settings

### Basic Information

| Field | Recommended Value | Status |
|-------|------------------|--------|
| **Display Name** | ${profileSettings.name} | - |
| **Tagline** | ${profileSettings.tagline} | - |
| **About/Bio** | ${profileSettings.bio} | - |
| **Location** | Your location | - |
| **Website** | ${profileSettings.website} | ⚠️ CRITICAL |

### Social Links

| Platform | URL |
|----------|-----|
| **Twitter** | https://twitter.com/${profileSettings.social.twitter.replace('@', '')} |
| **GitHub** | https://github.com/${profileSettings.social.github} |
| **LinkedIn** | ${profileSettings.social.linkedin || 'Add your LinkedIn URL'} |
| **Website** | ${profileSettings.social.website} |

### Publication Settings

If you have a publication:

| Field | Recommended Value |
|-------|------------------|
| **Publication Title** | ${profileSettings.name}'s Blog |
| **Description** | ${profileSettings.seo.description} |
| **Website URL** | ${profileSettings.website} |
| **Favicon** | Upload from ericgrill.com |
| **Logo** | Your personal logo |
| **Meta Title** | ${profileSettings.seo.title} |
| **Meta Description** | ${profileSettings.seo.description} |

### Custom Domain Setup (Optional but Recommended)

1. Go to Publication Settings → Custom Domain
2. Enter: blog.ericgrill.com (or subdomain)
3. Add DNS records as instructed
4. SSL certificate will be auto-generated

## SEO Checklist

### Profile
- [ ] Display name is your real name
- [ ] Tagline includes keywords
- [ ] Bio is 150+ characters
- [ ] Website URL is ericgrill.com
- [ ] All social links filled
- [ ] Profile picture is professional
- [ ] Cover image uploaded

### Blog Settings
- [ ] Meta title includes your name + keywords
- [ ] Meta description is compelling
- [ ] OG image is set (for social shares)
- [ ] Custom domain configured (optional)
- [ ] Newsletter enabled (builds audience)

### Content
- [ ] Write 3+ articles with canonical URLs to ericgrill.com
- [ ] Enable "Show in feed" for visibility
- [ ] Add cover images to all posts
- [ ] Use relevant tags (3-5 per post)
- [ ] Enable comments for engagement
`;
  
  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), profileGuide);
  
  // Generate publication setup guide
  const publicationGuide = `# Hashnode Publication Setup

## Creating a Publication

1. Go to https://hashnode.com/create-publication
2. Fill in details:
   - **Name:** ${profileSettings.name}'s Engineering Blog
   - **Description:** ${profileSettings.seo.description}
   - **URL:** hashnode.com/@${username}

## Publication Branding

### Logo & Favicon
- Upload your logo (recommended: 400x400px)
- Upload favicon from ericgrill.com

### Colors
- Primary color: Match ericgrill.com brand
- Accent color: Complementary color

### Custom CSS (Optional)
\`\`\`css
/* Add custom styles to match your brand */
.blog-post-content a {
  color: #your-brand-color;
}
\`\`\`

## Navigation Setup

Add these navigation items:

| Label | URL |
|-------|-----|
| Home | / |
| About | /about |
| Portfolio | https://ericgrill.com/projects |
| Contact | https://ericgrill.com/contact |
| Website | https://ericgrill.com |

## Widgets (Sidebar)

Enable these widgets:
- [ ] Newsletter signup
- [ ] About (short bio + link to website)
- [ ] Social links
- [ ] Recent posts
- [ ] Tags
`;
  
  await fs.writeFile(path.join(outputDir, 'publication-setup.md'), publicationGuide);
  
  // Generate article template
  const articleTemplate = `# Hashnode Article Template

## Template with Backlink

\`\`\`markdown
---
title: "Your Article Title"
subtitle: "A compelling subtitle for SEO"
description: "Meta description for search engines"
tags: [javascript, react, webdev, programming, software]
coverImage: "https://ericgrill.com/images/article-cover.jpg"
canonicalUrl: https://ericgrill.com/blog/article-slug
---

## Introduction

[Hook the reader]

## Main Content

[Your valuable content here]

## Code Examples

\`\`\`javascript
// Your code here
\`\`\`

## Conclusion

[Summarize key points]

---

## About the Author

**${profileSettings.name}** is a software engineer building innovative solutions.

🌐 **Website:** [ericgrill.com](https://ericgrill.com)
🐦 **Twitter:** [@${profileSettings.social.twitter.replace('@', '')}](https://twitter.com/${profileSettings.social.twitter.replace('@', '')})
💼 **LinkedIn:** [${profileSettings.social.github}](${profileSettings.social.linkedin || '#'})

*Subscribe to my newsletter on [ericgrill.com](https://ericgrill.com) for weekly insights.*
\`\`\`

## Backlink Placement Strategy

### In-Article Links
- Link to relevant projects on ericgrill.com
- Reference other articles with canonical URLs
- Add "Related reading" section

### Author Bio
Always include at the end:
- Name + title
- Website link (ericgrill.com)
- Social links
- Call to action (newsletter, contact)

### Comment Strategy
- Respond to all comments
- Include website link in signature when relevant
- Build relationships with other writers
`;
  
  await fs.writeFile(path.join(outputDir, 'article-template.md'), articleTemplate);
  
  // Try to fetch publication data if token available
  if (token) {
    try {
      const query = \`
        query GetUser {
          me {
            id
            name
            username
            publication {
              id
              title
              url
            }
          }
        }
      \`;
      
      const response = await axios.post(
        HASHNODE_API,
        { query },
        { headers: { Authorization: token } }
      );
      
      if (response.data?.data?.me) {
        await fs.writeJson(path.join(outputDir, 'current-profile.json'), response.data.data.me, { spaces: 2 });
        
        return {
          status: 'success',
          automated: true,
          profile: response.data.data.me,
          outputs: [
            'output/hashnode/profile-checklist.md',
            'output/hashnode/publication-setup.md',
            'output/hashnode/article-template.md'
          ]
        };
      }
    } catch (error) {
      console.log(\`   ⚠️  Hashnode API error: \${error.message}\`);
    }
  }
  
  // Save settings for manual reference
  await fs.writeJson(path.join(outputDir, 'profile-settings.json'), profileSettings, { spaces: 2 });
  
  return {
    status: 'manual_required',
    automated: false,
    message: 'Token not provided or invalid. Manual setup required.',
    outputs: [
      'output/hashnode/profile-checklist.md',
      'output/hashnode/publication-setup.md',
      'output/hashnode/article-template.md',
      'output/hashnode/profile-settings.json'
    ]
  };
}
