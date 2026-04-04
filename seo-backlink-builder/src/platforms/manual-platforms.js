import { config } from 'dotenv';
import fs from 'fs-extra';
import path from 'path';

config();

export async function generateManualGuides() {
  const platforms = [
    { id: 'producthunt', name: 'ProductHunt', fn: generateProductHuntGuide },
    { id: 'indiehackers', name: 'IndieHackers', fn: generateIndieHackersGuide },
    { id: 'stackoverflow', name: 'Stack Overflow', fn: generateStackOverflowGuide },
    { id: 'linkedin', name: 'LinkedIn', fn: generateLinkedInGuide },
    { id: 'twitter', name: 'Twitter/X', fn: generateTwitterGuide },
    { id: 'crunchbase', name: 'Crunchbase', fn: generateCrunchbaseGuide }
  ];
  
  for (const platform of platforms) {
    const outputDir = \`./output/\${platform.id}\`;
    await fs.ensureDir(outputDir);
    await platform.fn(outputDir);
  }
  
  return { generated: platforms.length };
}

async function generateProductHuntGuide(outputDir) {
  const guide = \`# ProductHunt Profile Optimization

## Profile Setup

### Step 1: Create/Claim Profile
1. Go to https://www.producthunt.com/
2. Sign up with email or social login
3. Verify your account via email

### Step 2: Complete Profile

| Field | Recommended Value |
|-------|------------------|
| **Name** | \${process.env.PERSONAL_NAME || 'Eric Grill'} |
| **Username** | \${process.env.GITHUB_USERNAME || 'ericgrill'} |
| **Headline** | \${process.env.BIO_SHORT || 'Software Engineer | Building the Future'} |
| **About** | \${process.env.BIO_LONG || 'Full-stack developer...'} |
| **Website** | https://ericgrill.com ⚠️ |
| **Twitter** | @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'} |
| **LinkedIn** | Add LinkedIn URL |

### Step 3: Upload Assets
- **Avatar:** Professional headshot (400x400px)
- **Cover:** Custom banner (1500x500px) with website URL

## Maker Profile Optimization

### Bio Structure
\`\`\`
👋 I'm Eric, a software engineer building [ericgrill.com](https://ericgrill.com)

🔭 Currently working on: [Project Name]
🌱 Learning: Blockchain, AI/ML
💬 Ask me about: Full-stack development
📫 Reach me: https://ericgrill.com/contact
\`\`\`

### Achievements to Highlight
- [ ] Products launched
- [ ] Upvotes received
- [ ] Maker rank
- [ ] Featured products

## Product Launch Strategy

### Launch Checklist
- [ ] Product page complete with ericgrill.com link
- [ ] Gallery images prepared
- [ ] Video demo recorded
- [ ] First comment prepared
- [ ] Social media ready for promotion
- [ ] Email list notified

### Product Page SEO
- **Name:** Clear and searchable
- **Tagline:** Include keywords + value proposition
- **Description:** 500+ words with ericgrill.com links
- **Website:** ericgrill.com or project URL
- **Maker:** Link to your profile

## Engagement Strategy

### Daily Actions
- [ ] Check notifications
- [ ] Upvote relevant products
- [ ] Comment thoughtfully on 3-5 products
- [ ] Respond to all comments on your products
- [ ] Share interesting finds on Twitter

### Weekly Actions
- [ ] Hunt 1-2 new products
- [ ] Write a review
- [ ] Connect with other makers
- [ ] Join relevant discussions
`;

  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), guide);
  
  const launchTemplate = \`# ProductHunt Launch Template

## Product Details

**Product Name:** Your Product Name
**Tagline:** One-line description with keywords
**Website:** https://ericgrill.com/product
**Category:** Developer Tools / Productivity / etc.

## Gallery

Prepare 5-10 images:
1. Hero image (main screenshot)
2. Feature highlights
3. Use case demos
4. Team photo (optional)
5. Social proof

## Description

\`\`\`
[Product Name] helps [target audience] achieve [benefit] through [key feature].

### Key Features

✨ Feature 1 - Brief description
✨ Feature 2 - Brief description
✨ Feature 3 - Brief description

### Why We Built This

[Your story - connect to ericgrill.com mission]

### Learn More

🌐 Website: https://ericgrill.com/product
🐦 Twitter: @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}
📧 Contact: https://ericgrill.com/contact
\`\`\`

## First Comment (By Maker)

\`\`\`
Hey ProductHunt! 👋

I'm Eric, the maker behind [Product]. I've been working on this for [time] because [problem you solved].

[Personal story - 2-3 sentences]

I'd love to hear your thoughts and feedback! 

🌐 Learn more: https://ericgrill.com
🐦 Follow my journey: @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}

What features would you like to see next?
\`\`\`
`;

  await fs.writeFile(path.join(outputDir, 'launch-template.md'), launchTemplate);
}

async function generateIndieHackersGuide(outputDir) {
  const guide = \`# IndieHackers Profile Optimization

## Profile Setup

### Step 1: Create Account
1. Go to https://www.indiehackers.com/
2. Sign up with email or social
3. Verify email address

### Step 2: Complete Profile

| Field | Recommended Value |
|-------|------------------|
| **Name** | \${process.env.PERSONAL_NAME || 'Eric Grill'} |
| **Username** | \${process.env.GITHUB_USERNAME || 'ericgrill'} |
| **Bio** | \${process.env.BIO_LONG || 'Software engineer...'} |
| **Location** | Your location |
| **Website** | https://ericgrill.com ⚠️ |
| **Twitter** | @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'} |
| **LinkedIn** | Your LinkedIn URL |
| **GitHub** | github.com/\${process.env.GITHUB_USERNAME || 'ericgrill'} |

### Step 3: Add Projects

Add ericgrill.com as a project:

| Field | Value |
|-------|-------|
| **Project Name** | EricGrill.com |
| **Tagline** | \${process.env.WEBSITE_TAGLINE || 'Personal website and portfolio'} |
| **URL** | https://ericgrill.com |
| **Status** | Live / In Progress |
| **Revenue** | Select as appropriate |
| **Category** | Developer Tools / SaaS / etc. |

## Content Strategy

### Post Types That Work Well

1. **Milestones** - Launch, revenue, user count
2. **Lessons Learned** - Failures and successes
3. **Build in Public** - Development updates
4. **Ask for Help** - Community engagement
5. **Resources** - Tools, guides, templates

### Post Template with Backlink

\`\`\`
**Title:** [Specific, benefit-driven headline]

[Opening hook - 2-3 sentences]

**Background**
[Context and story]

**What I Built**
[Description with link to ericgrill.com/project]

**Key Learnings**
- Learning 1
- Learning 2
- Learning 3

**Next Steps**
[What's coming next]

---

🔗 Check it out: https://ericgrill.com/project
🐦 Follow my journey: @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}

What would you do differently?
\`\`\`

## Engagement Tactics

### Daily
- [ ] Check "Newest" posts
- [ ] Comment on 3-5 relevant posts
- [ ] Respond to comments on your posts
- [ ] Join group discussions

### Weekly
- [ ] Post a milestone or update
- [ ] Share a resource
- [ ] Connect with 2-3 new indie hackers
- [ ] Participate in group challenges

## SEO Benefits

- Profile links are dofollow
- High domain authority (DA 60+)
- Indexed quickly
- Community engagement drives visibility
`;

  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), guide);
  
  const postTemplates = \`# IndieHackers Post Templates

## Template 1: Launch Post

\`\`\`
🚀 Just launched [Project] on [Platform]!

After [time] of building, it's finally live.

**What it does:**
[2-3 sentences describing value]

**Tech stack:**
- Tech 1
- Tech 2
- Tech 3

**Live at:** https://ericgrill.com/project

Would love your feedback!
\`\`\`

## Template 2: Milestone Post

\`\`\`
📈 Milestone: [Achievement]!

[Story of how you got here]

**Key takeaways:**
1. Takeaway 1
2. Takeaway 2
3. Takeaway 3

**What's next:**
[Future plans]

Full story: https://ericgrill.com/blog/milestone
\`\`\`

## Template 3: Lessons Learned

\`\`\`
💡 [Number] Lessons from [Experience]

I spent [time] working on [thing]. Here's what I learned:

1. **Lesson 1**
   Explanation...

2. **Lesson 2**
   Explanation...

3. **Lesson 3**
   Explanation...

Full write-up: https://ericgrill.com/blog/lessons
\`\`\`

## Template 4: Resource Share

\`\`\`
📚 I created a [resource] for [audience]

**What's included:**
- Item 1
- Item 2
- Item 3

**Get it here:** https://ericgrill.com/resource

Hope it helps! Let me know what you'd add.
\`\`\`
`;

  await fs.writeFile(path.join(outputDir, 'post-templates.md'), postTemplates);
}

async function generateStackOverflowGuide(outputDir) {
  const guide = \`# Stack Overflow Profile Optimization

## Profile Setup

### Step 1: Create/Login
1. Go to https://stackoverflow.com/
2. Create account or login
3. Verify email

### Step 2: Developer Story (Critical for SEO)

Navigate to: https://stackoverflow.com/story/

| Section | Content |
|---------|---------|
| **Name** | \${process.env.PERSONAL_NAME || 'Eric Grill'} |
| **Title** | \${process.env.BIO_SHORT || 'Software Engineer'} |
| **Location** | Your location |
| **Website** | https://ericgrill.com ⚠️ |
| **Twitter** | @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'} |
| **GitHub** | github.com/\${process.env.GITHUB_USERNAME || 'ericgrill'} |
| **About Me** | \${process.env.BIO_LONG || 'Full-stack developer...'} |

### Step 3: Add Experience

Add your work history with ericgrill.com projects:

\`\`\`
Title: Founder & Developer
Company: EricGrill.com
Website: https://ericgrill.com
Duration: [Start] - Present
Description: Building innovative software solutions and sharing knowledge through technical writing.
\`\`\`

### Step 4: Featured Tags

Add relevant tags for visibility:
- javascript
- reactjs
- node.js
- typescript
- web-development
- software-engineering

## SEO Benefits

- Stack Overflow has DA 90+
- Profile links are dofollow
- Developer Story ranks well in Google
- High trust domain

## Engagement Strategy

### Answer Questions
1. Search for questions in your expertise
2. Provide thorough, helpful answers
3. Include code examples
4. Link to ericgrill.com when relevant (don't spam)

### Ask Questions
- Ask genuine technical questions
- Link to your research on ericgrill.com
- Accept and upvote good answers

### Build Reputation
- Start with easier questions
- Build to 100+ reputation
- Unlock more privileges
- Profile becomes more visible
`;

  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), guide);
}

async function generateLinkedInGuide(outputDir) {
  const guide = \`# LinkedIn Profile Optimization

## Profile Setup

### Step 1: Basics
1. Go to https://linkedin.com
2. Complete profile to "All-Star" status

### Step 2: Contact Info

| Field | Value |
|-------|-------|
| **Profile URL** | linkedin.com/in/\${process.env.GITHUB_USERNAME || 'ericgrill'} |
| **Website** | https://ericgrill.com |
| **Website Label** | "Personal Website" or "Portfolio" |
| **Email** | Your email |
| **Twitter** | @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'} |

### Step 3: Headline

**Current:** Default job title
**Optimized:** \${process.env.BIO_SHORT || 'Software Engineer | Building ericgrill.com | Full-Stack Developer'}

### Step 4: About Section

\`\`\`
\${process.env.BIO_LONG || 'Full-stack developer passionate about creating technology that makes a difference.'}

I specialize in:
• Modern JavaScript/TypeScript ecosystems
• React and Node.js applications
• Scalable system architecture
• Open source contributions

Currently building https://ericgrill.com - my personal platform for sharing software engineering insights and projects.

Let's connect! I'm always interested in discussing:
→ Software architecture and best practices
→ Startup technology challenges
→ Open source collaboration
→ Mentorship opportunities

📧 Contact: [your-email]
🌐 Website: https://ericgrill.com
🐦 Twitter: @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'}
\`\`\`

### Step 5: Experience

Add ericgrill.com as current position:

\`\`\`
Title: Founder & Lead Developer
Company: EricGrill.com (Self-employed)
Duration: [Start Date] - Present
Location: [Your Location]
Description:
• Building and maintaining ericgrill.com - personal portfolio and blog platform
• Developing full-stack applications using React, Node.js, and modern cloud infrastructure
• Writing technical content on software engineering best practices
• Contributing to open source projects
• [Other achievements]
\`\`\`

### Step 6: Featured Section

Add to Featured:
- [ ] Link to ericgrill.com
- [ ] Link to GitHub profile
- [ ] Link to latest project
- [ ] Link to popular article

## SEO Checklist

- [ ] Custom profile URL set
- [ ] Website link in contact info
- [ ] ericgrill.com mentioned in About
- [ ] ericgrill.com in Experience
- [ ] Featured section has website link
- [ ] Headline includes keywords
- [ ] Skills section complete (50+)
- [ ] Recommendations received (3+)

## Content Strategy

### Weekly Posts
- Share blog posts from ericgrill.com
- Comment on industry news
- Share project updates
- Post helpful resources

### Engagement
- Comment on posts in your network
- Join relevant groups
- Answer questions in your expertise
- Congratulate connections on milestones
`;

  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), guide);
}

async function generateTwitterGuide(outputDir) {
  const guide = \`# Twitter/X Profile Optimization

## Profile Setup

### Step 1: Basics
1. Go to https://twitter.com
2. Navigate to Edit Profile

### Step 2: Profile Fields

| Field | Recommended Value |
|-------|------------------|
| **Name** | \${process.env.PERSONAL_NAME || 'Eric Grill'} |
| **Bio** | \${process.env.BIO_SHORT || 'Software Engineer'} 🌐 ericgrill.com |
| **Location** | Your location |
| **Website** | https://ericgrill.com |
| **Birth date** | [Your birthday] |

### Step 3: Visuals

- **Profile photo:** Professional headshot (400x400px)
- **Header image:** 1500x500px with branding
  - Include ericgrill.com URL on header
  - Consistent with website branding

## Bio Optimization

### Current Examples

**Good:**
\`\`\`
Software Engineer • Building @ericgrillcom • React • Node.js • Writing about web dev 🌐 ericgrill.com
\`\`\`

**Better:**
\`\`\`
👨‍💻 Building the future of tech at ericgrill.com
🚀 Full-stack • React • Node.js • AI
✍️ Writing about software engineering
🌐 https://ericgrill.com
\`\`\`

## Pinned Tweet Strategy

Create a pinned tweet that:
- Introduces who you are
- Links to ericgrill.com
- Highlights your best work
- Includes call to action

**Template:**
\`\`\`
👋 Hey, I'm Eric!

I'm a software engineer building [what you build].

🌐 Check out my work: https://ericgrill.com
📝 Read my writing: https://ericgrill.com/blog
💻 See my code: github.com/\${process.env.GITHUB_USERNAME || 'ericgrill'}

Follow along as I build in public! 🚀
\`\`\`

## Content Strategy

### Tweet Types

1. **Build in Public** - Share progress screenshots
2. **Educational** - Tips and tutorials
3. **Thread** - Deep dives linking to ericgrill.com
4. **Engagement** - Reply to relevant tweets
5. **Promotion** - New blog posts, projects

### Daily Routine
- [ ] Check notifications
- [ ] Reply to 5-10 relevant tweets
- [ ] Post 1-2 original tweets
- [ ] Share something from ericgrill.com

### Weekly Routine
- [ ] Write 1 thread
- [ ] Engage with 3-5 larger accounts
- [ ] Share blog post
- [ ] Update pinned if needed

## Link Strategy

### In Bio
- Primary: ericgrill.com
- Use link shortener or direct URL

### In Tweets
- Link to ericgrill.com/blog posts
- Use cards for better preview
- Pin important links

### In Threads
- End with CTA to website
- Link relevant resources
- Build email list from traffic
`;

  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), guide);
}

async function generateCrunchbaseGuide(outputDir) {
  const guide = \`# Crunchbase Profile Optimization

## Profile Setup

### Step 1: Create Account
1. Go to https://www.crunchbase.com/
2. Sign up with LinkedIn or email
3. Verify email address

### Step 2: Person Profile

Navigate to: https://www.crunchbase.com/me/edit

| Field | Value |
|-------|-------|
| **Name** | \${process.env.PERSONAL_NAME || 'Eric Grill'} |
| **Title** | \${process.env.BIO_SHORT || 'Software Engineer'} |
| **Company** | EricGrill.com |
| **Location** | Your location |
| **Biography** | \${process.env.BIO_LONG || 'Full-stack developer...'} |
| **Website** | https://ericgrill.com |
| **LinkedIn** | Your LinkedIn URL |
| **Twitter** | @\${process.env.PERSONAL_TWITTER?.replace('@', '') || 'ericgrill'} |

### Step 3: Add Organization

If applicable, add ericgrill.com as an organization:

| Field | Value |
|-------|-------|
| **Organization Name** | EricGrill.com |
| **Website** | https://ericgrill.com |
| **Description** | \${process.env.WEBSITE_DESCRIPTION || 'Personal website and portfolio'} |
| **Categories** | Software, Internet, Developer Tools |
| **Founder** | \${process.env.PERSONAL_NAME || 'Eric Grill'} |

## SEO Benefits

- Crunchbase has DA 90+
- Profile links are dofollow
- Ranks well for name searches
- Trusted by Google Knowledge Graph

## Additional Platforms to Consider

### AngelList / Wellfound
- https://angel.co/
- Add ericgrill.com as project
- Link in bio

### BetaList
- https://betalist.com/
- Submit projects for early adopters
- Profile links to website

### Hacker News
- https://news.ycombinator.com/
- Add website to profile
- Participate in discussions
- Submit Show HN posts

### Reddit
- r/webdev, r/javascript, r/reactjs
- Add website to profile
- Participate authentically
- Share valuable content

### Discord Communities
- Reactiflux
- Node.js
- Various startup servers
- Add website to profile

### Slack Communities
- Indie Hackers
- Makerlog
- Various niche communities
- Add website to profile
`;

  await fs.writeFile(path.join(outputDir, 'profile-checklist.md'), guide);
}
