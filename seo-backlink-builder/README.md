# SEO Backlink Builder for ericgrill.com

A comprehensive toolkit for building backlinks to ericgrill.com across developer platforms.

## Overview

This toolkit helps optimize and create profiles on developer-focused platforms to build backlinks to ericgrill.com. It uses a hybrid approach:
- **Automated**: GitHub profile optimization, metadata generation
- **Semi-automated**: API-based platforms (where credentials are provided)
- **Manual guidance**: Platforms requiring human verification (CAPTCHA, email confirmation)

## Platforms Targeted

| Platform | Type | Automation Level | Status |
|----------|------|------------------|--------|
| GitHub | Profile/Bio | Automated | ✅ Ready |
| Dev.to | Profile/Publications | API-based | ⚠️ Needs Token |
| Hashnode | Profile/Blog | API-based | ⚠️ Needs Token |
| ProductHunt | Maker Profile | Manual + Guidance | ⚠️ OAuth Required |
| IndieHackers | Profile | Manual + Guidance | ⚠️ Login Required |
| Stack Overflow | Developer Story | Manual + Guidance | ⚠️ Login Required |
| LinkedIn | Profile | Manual + Guidance | ⚠️ Login Required |
| Twitter/X | Bio/Profile | Manual + Guidance | ⚠️ Login Required |
| Crunchbase | Person Profile | Manual + Guidance | ⚠️ Login Required |

## Quick Start

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env

# Run the full optimization suite
npm run optimize

# Or run specific modules
npm run optimize:github
npm run optimize:devto
npm run optimize:hashnode
npm run report
```

## Environment Setup

Create a `.env` file with your credentials:

```env
# GitHub (Required for GitHub optimization)
GITHUB_TOKEN=ghp_your_personal_access_token
GITHUB_USERNAME=ericgrill

# Dev.to (Required for Dev.to API)
DEVTO_API_KEY=your_devto_api_key

# Hashnode (Required for Hashnode API)
HASHNODE_TOKEN=your_hashnode_token
HASHNODE_USERNAME=ericgrill

# Personal Info (Used across platforms)
PERSONAL_NAME=Eric Grill
PERSONAL_EMAIL=your@email.com
PERSONAL_TWITTER=@ericgrill
PERSONAL_LINKEDIN=linkedin.com/in/ericgrill
WEBSITE_URL=https://ericgrill.com
WEBSITE_TAGLINE="Building the future of technology"
WEBSITE_DESCRIPTION="Eric Grill's personal website and portfolio"

# Content
BIO_SHORT="Software engineer building innovative solutions"
BIO_LONG="Full-stack developer passionate about creating impactful technology. I write about software engineering, startups, and the future of tech."
```

## Getting API Tokens

### GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Scopes needed: `read:user`, `user:email`, `read:org`
4. Copy token to `.env`

### Dev.to API Key
1. Go to https://dev.to/settings/extensions
2. Generate API Key
3. Copy to `.env`

### Hashnode Token
1. Go to https://hashnode.com/settings/developer
2. Generate Personal Access Token
3. Copy to `.env`

## Generated Assets

Running the optimization creates:

```
output/
├── github/
│   ├── profile-optimized.md      # Optimized GitHub profile README
│   └── seo-analysis.json         # SEO analysis results
├── devto/
│   ├── profile-settings.json     # Profile optimization suggestions
│   └── articles-template.md      # Article templates with backlinks
├── hashnode/
│   ├── profile-settings.json     # Profile optimization suggestions
│   └── publication-template.md   # Publication setup guide
├── producthunt/
│   ├── profile-checklist.md      # Profile creation checklist
│   └── launch-template.md        # Product launch template
├── indiehackers/
│   ├── profile-checklist.md      # Profile optimization checklist
│   └── post-templates.md         # Post templates with backlinks
├── link-report.json              # Complete backlink report
└── submission-tracker.csv        # Track all submissions
```

## Manual Platform Checklists

For platforms that require manual setup, detailed checklists are generated in `output/`. These include:
- Exact fields to fill
- SEO-optimized copy suggestions
- Screenshot references for navigation
- Verification steps

## Compliance & Best Practices

- ✅ Only creates/optimizes profiles you own
- ✅ Uses official APIs where available
- ✅ Respects rate limits
- ✅ No credential storage (uses env vars)
- ✅ Generates human-friendly reports

## License

MIT - Use responsibly and in accordance with each platform's Terms of Service.
