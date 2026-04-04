import { config } from 'dotenv';
import axios from 'axios';
import fs from 'fs-extra';
import path from 'path';

config();

const DEVTO_API_BASE = 'https://dev.to/api';

export async function optimizeDevTo() {
  const apiKey = process.env.DEVTO_API_KEY;
  const outputDir = './output/devto';
  
  await fs.ensureDir(outputDir);
  
  const profileTemplate = {
    username: process.env.GITHUB_USERNAME || 'ericgrill',
    name: process.env.PERSONAL_NAME || 'Eric Grill',
    summary: process.env.BIO_SHORT || 'Software engineer building the future',
    website_url: process.env.WEBSITE_URL || 'https://ericgrill.com',
    location: '',
    education: '',
    employer_name: '',
    employer_title: '',
    looking_for_work: false
  };
  
  // Generate profile optimization guide
  const profileGuide = `# Dev.to Profile Optimization Guide

## Profile Settings

Visit: https://dev.to/settings

### Basic Fields

| Field | Recommended Value | Current |
|-------|------------------|---------|
| **Name** | ${profileTemplate.name} | - |
| **Username** | ${profileTemplate.username} | - |
| **Email** | ${process.env.PERSONAL_EMAIL || 'your@email.com'} | - |
| **Website URL** | ${profileTemplate.website_url} | ⚠️ CRITICAL |
| **Location** | Your location | - |
| **Bio** | ${profileTemplate.summary} | - |
| **Education** | Your education | - |
| **Currently learning** | Blockchain, AI/ML, etc. | - |
| **Currently hacking on** | ${profileTemplate.website_url} | - |
| **Available for** | Consulting, collaborations | - |

### Branding

| Field | Recommendation |
|-------|---------------|
| **Profile image** | Professional headshot |
| **Cover image** | Custom banner with branding |

## SEO Optimization Checklist

### Profile Setup
- [ ] Website URL points to ericgrill.com
- [ ] Bio includes relevant keywords (software, engineering, startup)
- [ ] Location filled for local SEO
- [ ] Profile image is professional
- [ ] Cover image includes website URL or branding

### Content Strategy
- [ ] Write 3-5 articles linking to ericgrill.com
- [ ] Use canonical URLs pointing to ericgrill.com for cross-posts
- [ ] Include website link in article footers
- [ ] Tag articles with relevant keywords
- [ ] Engage with community (comment, like, follow)

## Article Template

\`\`\`markdown
---
title: "Your Article Title"
published: true
description: "Brief description for SEO"
tags: javascript, react, webdev, programming
canonical_url: https://ericgrill.com/blog/your-article
---

Your article content here...

---

*This article was originally published on [ericgrill.com](https://ericgrill.com).*

Connect with me:
- 🌐 [Website](https://ericgrill.com)
- 🐦 [Twitter](https://twitter.com/${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'})
- 💼 [LinkedIn](https://linkedin.com/in/${process.env.GITHUB_USERNAME || 'ericgrill'})
\`\`\`

## Organization Setup

If you have a company/project:
1. Go to https://dev.to/organization-info
2. Create organization
3. Add ericgrill.com as website
4. Post articles under org for additional exposure
`;
  
  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), profileGuide);
  
  // Generate article templates with backlinks
  const articleTemplates = `# Article Templates with Backlinks

## Template 1: Technical Tutorial

\`\`\`markdown
---
title: "Building Scalable Applications with Modern Stack"
published: false
description: "Learn how to build scalable web applications using the latest technologies"
tags: javascript, scalability, architecture, tutorial
canonical_url: https://ericgrill.com/blog/scalable-applications
---

## Introduction

In this tutorial, we'll explore...

[Your content here]

## Conclusion

Building scalable applications requires...

---

*Want to learn more? Check out my other articles on [ericgrill.com](https://ericgrill.com).*

**About the Author:**
Eric Grill is a software engineer building innovative solutions. 
Visit [ericgrill.com](https://ericgrill.com) for more content.

Follow me on [Twitter](https://twitter.com/${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}) for daily tips.
\`\`\`

## Template 2: Career/Experience Post

\`\`\`markdown
---
title: "Lessons Learned from 10 Years in Software Engineering"
published: false
description: "Key insights from a decade of building software products"
tags: career, softwareengineering, experience, lessons
canonical_url: https://ericgrill.com/blog/10-years-engineering
---

## My Journey

[Your story]

## Key Lessons

1. Lesson one
2. Lesson two
3. Lesson three

---

*Read more career insights on [ericgrill.com/career](https://ericgrill.com).*

**Connect with me:**
- 🌐 Website: [ericgrill.com](https://ericgrill.com)
- 🐦 Twitter: @${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}
- 💼 LinkedIn: [linkedin.com/in/${process.env.GITHUB_USERNAME || 'ericgrill'}](https://linkedin.com/in/${process.env.GITHUB_USERNAME || 'ericgrill'})
\`\`\`

## Template 3: Project Showcase

\`\`\`markdown
---
title: "Showcase: Building ${process.env.WEBSITE_TAGLINE || 'My Latest Project'}"
published: false
description: "A deep dive into my latest project and the technology behind it"
tags: showdev, javascript, opensource, project
canonical_url: https://ericgrill.com/projects/latest
---

## Project Overview

[Project description]

## Tech Stack

- Technology 1
- Technology 2

## Live Demo

🌐 [View Live](https://ericgrill.com/projects/demo)

## Source Code

💻 [GitHub](https://github.com/${process.env.GITHUB_USERNAME || 'ericgrill'}/project)

---

*Explore more projects on [ericgrill.com/projects](https://ericgrill.com/projects)*
\`\`\`
`;
  
  await fs.writeFile(path.join(outputDir, 'article-templates.md'), articleTemplates);
  
  // Try to fetch actual profile if API key available
  if (apiKey) {
    try {
      const response = await axios.get(`${DEVTO_API_BASE}/articles/me`, {
        headers: { 'api-key': apiKey }
      });
      
      await fs.writeJson(path.join(outputDir, 'current-articles.json'), response.data, { spaces: 2 });
      
      return {
        status: 'success',
        automated: true,
        articles: response.data.length,
        outputs: ['output/devto/profile-checklist.md', 'output/devto/article-templates.md']
      };
    } catch (error) {
      console.log(`   ⚠️  Dev.to API error: ${error.message}`);
    }
  }
  
  // Save profile settings for manual reference
  await fs.writeJson(path.join(outputDir, 'profile-settings.json'), profileTemplate, { spaces: 2 });
  
  return {
    status: 'manual_required',
    automated: false,
    message: 'API key not provided or invalid. Manual setup required.',
    outputs: ['output/devto/profile-checklist.md', 'output/devto/article-templates.md', 'output/devto/profile-settings.json']
  };
}
