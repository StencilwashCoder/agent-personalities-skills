# AI Repository Research Pipeline

A 24/7 autonomous research system that discovers, analyzes, and documents trending AI repositories from GitHub.

## Overview

This skill provides a continuous research pipeline that:

- 🔍 **Discovers** trending AI repositories from multiple sources
- 🧠 **Researches** each repository using LLM-powered analysis
- 📝 **Documents** findings with structured markdown reports
- 🌐 **Publishes** a static site with all research
- 📊 **Tracks** repositories in MinIO for persistence

## Features

- **Autonomous Discovery**: Finds new AI repos from GitHub trending, Hacker News, and curated lists
- **Deep Research**: Generates comprehensive analysis including:
  - Architecture overview
  - Key features and capabilities
  - Use cases and target audience
  - Technical implementation details
  - Comparison with alternatives
- **Static Site Generation**: Builds a searchable, filterable research site
- **Queue Management**: MinIO-backed queue for reliable processing
- **Parallel Processing**: Efficient batch processing of repositories

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Discovery     │────▶│  Research Queue │────▶│  Deep Analysis  │
│   (GitHub/HN)   │     │    (MinIO S3)   │     │    (Gemini)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Static Site    │
                                               │  Generator      │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  S3 Deployment  │
                                               │  (chainbytes.io)│
                                               └─────────────────┘
```

## Directory Structure

```
skills/ai-repo-research/
├── scripts/
│   ├── research-pipeline.sh      # Main pipeline orchestrator
│   ├── discover-repos.py         # Repository discovery
│   ├── research-repo.py          # Single repo deep research
│   └── generate-site.py          # Static site generator
├── templates/
│   └── site-template.html        # Site HTML template
├── data/                         # MinIO-backed storage
└── README.md                     # This file
```

## Usage

### Run Full Pipeline

```bash
./scripts/research-pipeline.sh
```

### Discover New Repos Only

```bash
python3 scripts/discover-repos.py --count 10
```

### Research Single Repo

```bash
python3 scripts/research-repo.py --owner "karpathy" --repo "minGPT"
```

### Generate Site Only

```bash
python3 scripts/generate-site.py
```

## Configuration

Environment variables:

```bash
export GITHUB_TOKEN="your_github_token"
export GEMINI_API_KEY="your_gemini_api_key"
export MINIO_ENDPOINT="https://s3.chainbytes.io"
export MINIO_ACCESS_KEY="chainbytes"
export MINIO_SECRET_KEY="chainbytes2026"
```

## Research Site

Live research outputs: https://s3.chainbytes.io/research-site/index.html

## Stats

- Repos processed per hour: 5
- Target: 120 repos/day
- Discovery sources: GitHub Trending, Hacker News, curated lists

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

Eric Grill / PatchRat
