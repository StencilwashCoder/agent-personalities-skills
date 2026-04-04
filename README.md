<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-191919?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Agents-136-58A6FF?style=for-the-badge" alt="136 Agents">
  <img src="https://img.shields.io/badge/Personalities-30-F78166?style=for-the-badge" alt="30 Personalities">
  <img src="https://img.shields.io/badge/Skills-4-3FB950?style=for-the-badge" alt="4 Skills">
</p>

<h1 align="center">Agent Personalities & Skills</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=22&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=600&lines=136+Specialized+Agents;30+Unique+Personalities;Installable+Claude+Code+Plugin;Drop+In+%26+Go" alt="Typing SVG" />
</p>

<p align="center">
  <strong>A curated library of AI agent definitions, personalities, and reusable skills for Claude Code.</strong><br>
  Install as a plugin or copy individual agents into your workflow.
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-agents-136">Agents</a> •
  <a href="#-personalities-30">Personalities</a> •
  <a href="#-skills">Skills</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## ⚡ Quick Start

### Install as Claude Code Plugin

```bash
# Add to your Claude Code plugin marketplace, then:
/plugin install agent-personalities-skills
```

### Use Individual Agents

Copy any agent `.md` file from `agents/` into your project's `.claude/agents/` directory:

```bash
# Example: add the backend-developer agent
cp agents/core-dev/backend-developer.md .claude/agents/
```

### Use a Personality

```bash
# Paste into your AI assistant's system prompt
cat personalities/general/architecture-astronaut.md
```

---

## 🤖 Agents (136)

All agents use Claude Code SDK format — YAML frontmatter with `name`, `description`, `tools`, and `model`, followed by a system prompt. Drop them into `agents/` and they're ready.

### Core Development

<p>
  <img src="https://img.shields.io/badge/core--dev-10_agents-58A6FF?style=flat-square" alt="core-dev">
</p>

| Agent | Description |
|-------|-------------|
| `api-designer` | REST/GraphQL endpoint design, OpenAPI docs, auth patterns, versioning |
| `backend-developer` | Server-side APIs, microservices, scalability, production-ready systems |
| `electron-pro` | Electron desktop apps, native OS integration, cross-platform distribution |
| `frontend-developer` | React, Vue, Angular — multi-framework frontend expertise |
| `fullstack-developer` | Complete features spanning database, API, and frontend layers |
| `graphql-architect` | GraphQL schemas, federation, query optimization across services |
| `microservices-architect` | Distributed systems, service decomposition, communication patterns |
| `mobile-developer` | React Native, Flutter — cross-platform with native performance |
| `ui-designer` | Visual interfaces, design systems, component libraries, accessibility |
| `websocket-engineer` | Real-time bidirectional communication at scale |

### Language Specialists

<p>
  <img src="https://img.shields.io/badge/lang-26_agents-58A6FF?style=flat-square" alt="lang">
</p>

| Agent | Agent | Agent |
|-------|-------|-------|
| `angular-architect` | `cpp-pro` | `csharp-developer` |
| `django-developer` | `dotnet-core-expert` | `dotnet-framework-4.8-expert` |
| `elixir-expert` | `flutter-expert` | `golang-pro` |
| `java-architect` | `javascript-pro` | `kotlin-specialist` |
| `laravel-specialist` | `nextjs-developer` | `php-pro` |
| `powershell-5.1-expert` | `powershell-7-expert` | `python-pro` |
| `rails-expert` | `react-specialist` | `rust-engineer` |
| `spring-boot-engineer` | `sql-pro` | `swift-expert` |
| `typescript-pro` | `vue-expert` | |

### Infrastructure

<p>
  <img src="https://img.shields.io/badge/infra-16_agents-58A6FF?style=flat-square" alt="infra">
</p>

| Agent | Description |
|-------|-------------|
| `azure-infra-engineer` | Azure networking, Entra ID, PowerShell, Bicep IaC |
| `cloud-architect` | Multi-cloud strategy, migrations, disaster recovery, cost optimization |
| `database-administrator` | Performance tuning, HA architectures, disaster recovery |
| `deployment-engineer` | CI/CD pipelines and deployment automation |
| `devops-engineer` | Infrastructure automation, containerization, delivery pipelines |
| `devops-incident-responder` | Production incident response, diagnosis, postmortems |
| `docker-expert` | Container images, orchestration, security hardening |
| `incident-responder` | Active breach response, evidence preservation, recovery |
| `kubernetes-specialist` | Cluster design, deployment, configuration, troubleshooting |
| `network-engineer` | Cloud and hybrid network design, security, performance |
| `platform-engineer` | Internal developer platforms, self-service infrastructure |
| `security-engineer` | Security controls, CI/CD hardening, zero-trust, compliance |
| `sre-engineer` | SLOs, error budgets, chaos engineering, toil reduction |
| `terraform-engineer` | Multi-cloud IaC, module architecture, state management |
| `terragrunt-expert` | DRY configurations, dependency management, multi-env deployments |
| `windows-infra-admin` | Windows Server, Active Directory, DNS, DHCP, Group Policy |

### Data & AI

<p>
  <img src="https://img.shields.io/badge/data--ai-12_agents-58A6FF?style=flat-square" alt="data-ai">
</p>

| Agent | Description |
|-------|-------------|
| `ai-engineer` | End-to-end AI systems — model selection to production deployment |
| `data-analyst` | Dashboards, reports, statistical analysis for decision-making |
| `data-engineer` | Pipelines, ETL/ELT, data infrastructure, quality management |
| `data-scientist` | Predictive models, exploratory analysis, hypothesis testing |
| `database-optimizer` | Slow query analysis, indexing strategies, cross-system optimization |
| `llm-architect` | LLM systems, fine-tuning, RAG, inference serving, multi-model |
| `machine-learning-engineer` | ML model deployment, optimization, serving at scale |
| `ml-engineer` | Training pipelines, model serving, automated retraining |
| `mlops-engineer` | ML infrastructure, CI/CD for models, experiment tracking |
| `nlp-engineer` | Text processing, NER, sentiment analysis, translation |
| `postgres-pro` | PostgreSQL performance, replication, backup, advanced features |
| `prompt-engineer` | Prompt design, optimization, testing, evaluation |

### Quality & Security

<p>
  <img src="https://img.shields.io/badge/qa--sec-14_agents-58A6FF?style=flat-square" alt="qa-sec">
</p>

| Agent | Description |
|-------|-------------|
| `accessibility-tester` | WCAG compliance, screen reader testing, inclusive design |
| `ad-security-reviewer` | Active Directory security review and hardening |
| `architect-reviewer` | Architecture review for scalability and maintainability |
| `chaos-engineer` | Fault injection, resilience testing, failure mode analysis |
| `code-reviewer` | Bug detection, logic errors, security vulnerabilities, quality |
| `compliance-auditor` | Regulatory compliance, audit trails, policy enforcement |
| `debugger` | Systematic bug hunting, root cause analysis |
| `error-detective` | Error pattern analysis, log investigation |
| `penetration-tester` | Authorized security testing, vulnerability assessment |
| `performance-engineer` | Load testing, profiling, bottleneck identification |
| `powershell-security-hardening` | PowerShell security policies and hardening |
| `qa-expert` | Test strategy, coverage analysis, quality assurance |
| `security-auditor` | Security review, threat modeling, vulnerability scanning |
| `test-automator` | Test automation frameworks, CI integration |

### Developer Experience

<p>
  <img src="https://img.shields.io/badge/dev--exp-13_agents-58A6FF?style=flat-square" alt="dev-exp">
</p>

| Agent | Description |
|-------|-------------|
| `build-engineer` | Build performance, compilation times, scaling build systems |
| `cli-developer` | Command-line tools, cross-platform CLIs, terminal UX |
| `dependency-manager` | Vulnerability audits, version conflicts, bundle optimization |
| `documentation-engineer` | API docs, tutorials, guides, developer content |
| `dx-optimizer` | Developer workflow optimization, feedback loops, satisfaction |
| `git-workflow-manager` | Git workflows, branching strategies, merge management |
| `legacy-modernizer` | Incremental migration, tech debt reduction, risk mitigation |
| `mcp-developer` | MCP servers and clients for AI-tool integration |
| `powershell-module-architect` | PowerShell module design, profile systems, packaging |
| `powershell-ui-architect` | WinForms, WPF, TUI for PowerShell automation |
| `refactoring-specialist` | Code transformation while preserving behavior |
| `slack-expert` | Slack apps, API integrations, bot development |
| `tooling-engineer` | Developer tools, code generators, IDE extensions |

### Business & Product

<p>
  <img src="https://img.shields.io/badge/biz-11_agents-58A6FF?style=flat-square" alt="biz">
</p>

| Agent | Description |
|-------|-------------|
| `business-analyst` | Process analysis, requirements gathering, improvement opportunities |
| `content-marketer` | Content strategy, SEO, multi-channel campaigns |
| `customer-success-manager` | Customer health, retention, upsell, lifetime value |
| `legal-advisor` | Contracts, compliance, IP protection, risk assessment |
| `product-manager` | Product strategy, feature prioritization, roadmap planning |
| `project-manager` | Project plans, risk management, budget, stakeholder coordination |
| `sales-engineer` | Technical pre-sales, solution architecture, POC development |
| `scrum-master` | Agile facilitation, sprint planning, velocity improvement |
| `technical-writer` | API references, user guides, SDK docs, getting-started guides |
| `ux-researcher` | User research, usability testing, persona development |
| `wordpress-master` | Custom themes/plugins, WooCommerce, headless WordPress |

### Specialized Domains

<p>
  <img src="https://img.shields.io/badge/domains-12_agents-58A6FF?style=flat-square" alt="domains">
</p>

| Agent | Description |
|-------|-------------|
| `api-documenter` | OpenAPI specs, interactive docs, code examples |
| `blockchain-developer` | Smart contracts, DApps, Solidity, gas optimization |
| `embedded-systems` | Firmware, RTOS, real-time systems, hardware constraints |
| `fintech-engineer` | Payment systems, compliance, secure transaction processing |
| `game-developer` | Game systems, graphics, multiplayer networking, gameplay |
| `iot-engineer` | Device management, edge computing, cloud integration |
| `m365-admin` | Exchange, Teams, SharePoint, Graph API automation |
| `mobile-app-developer` | iOS/Android apps, native features, platform UX |
| `payment-integration` | Payment gateways, PCI compliance, fraud prevention |
| `quant-analyst` | Trading strategies, financial models, derivatives pricing |
| `risk-manager` | Enterprise risk across financial, operational, regulatory domains |
| `seo-specialist` | Technical audits, keyword strategy, search rankings |

### Research & Analysis

<p>
  <img src="https://img.shields.io/badge/research-7_agents-58A6FF?style=flat-square" alt="research">
</p>

| Agent | Description |
|-------|-------------|
| `competitive-analyst` | Competitive landscape, market positioning, SWOT |
| `data-researcher` | Data collection, analysis, insight extraction |
| `market-researcher` | Market sizing, trends, customer segmentation |
| `research-analyst` | Deep research with source attribution and rigor |
| `scientific-literature-researcher` | Literature review, paper analysis, citation tracking |
| `search-specialist` | Advanced search techniques, information retrieval |
| `trend-analyst` | Trend identification, forecasting, signal detection |

### Meta-Orchestration

<p>
  <img src="https://img.shields.io/badge/meta-10_agents-58A6FF?style=flat-square" alt="meta">
</p>

| Agent | Description |
|-------|-------------|
| `agent-installer` | Agent installation and configuration |
| `agent-organizer` | Agent inventory management and categorization |
| `context-manager` | Shared context across agent interactions |
| `error-coordinator` | Cross-agent error handling and recovery |
| `it-ops-orchestrator` | IT operations workflow coordination |
| `knowledge-synthesizer` | Knowledge aggregation from multiple agents |
| `multi-agent-coordinator` | Multi-agent task orchestration |
| `performance-monitor` | Agent performance tracking and optimization |
| `task-distributor` | Task routing to appropriate agents |
| `workflow-orchestrator` | Complex workflow management across agents |

### Feature Development & Utilities

<p>
  <img src="https://img.shields.io/badge/feature--dev-3_agents-3FB950?style=flat-square" alt="feature-dev">
  <img src="https://img.shields.io/badge/code--simplifier-1_agent-3FB950?style=flat-square" alt="code-simplifier">
  <img src="https://img.shields.io/badge/superpowers-1_agent-3FB950?style=flat-square" alt="superpowers">
</p>

| Agent | Description |
|-------|-------------|
| `feature-dev/code-architect` | Architecture blueprints from codebase pattern analysis |
| `feature-dev/code-explorer` | Deep codebase analysis, execution path tracing |
| `feature-dev/code-reviewer` | Bug detection with confidence-based filtering |
| `code-simplifier/code-simplifier` | Simplifies code for clarity and maintainability |
| `superpowers/code-reviewer` | Code review against plans and coding standards |

---

## 🎭 Personalities (30)

Framework-agnostic system prompts that shape AI behavior. Copy the system prompt block into any AI assistant.

### Engineering Personalities

| Personality | Emoji | Description |
|-------------|:-----:|-------------|
| Architecture Astronaut | 🚀 | Detects and calls out over-engineering |
| Code Reviewer | 🔍 | Ruthless reviewer focused on quality |
| Debugger | 🐛 | Systematic bug hunter, root cause finder |
| Refactorer | 🔧 | Clean code specialist — transforms mess into maintainability |
| Performance Tuner | ⚡ | Finds and fixes performance bottlenecks |
| Security Sentinel | 🔒 | Security-focused code reviewer |
| Test-Driven Craftsman | 🔨 | Red-green-refactor, tests first |
| Test-Driven Maniac | 🧪 | Extreme TDD — won't write code without a failing test |
| Chaos Engineer | 💥 | Breaks things on purpose to build resilience |
| Concurrency Whisperer | 🔄 | Master of threads, async, and parallel execution |
| PatchRat | 🐀 | Hoards and applies patches with precision |

### Specialist Personalities

| Personality | Emoji | Description |
|-------------|:-----:|-------------|
| API Wrangler | 🔌 | Designs clean, intuitive APIs |
| API Migration Specialist | 🚚 | Moves systems between APIs safely |
| CLI Magician | 🪄 | Command-line tool wizard |
| Database Sage | 🗄️ | Database design and optimization oracle |
| Data Alchemist | 🧪 | Transforms raw data into actionable insights |
| Dependency Whisperer | 📦 | Tames dependency hell |
| DevOps Dispatcher | 🛠️ | Infrastructure and deployment expert |
| Documentation Writer | 📝 | Creates clear, comprehensive docs |
| Git Archaeologist | 📜 | Master of git history, digger of ancient commits |
| Legacy Archaeologist | 🏛️ | Excavates ancient, undocumented codebases |
| Legacy Code Archaeologist | ⛏️ | Deep-dive specialist for legacy systems |
| UX Psychic | 🔮 | Anticipates user friction, advocates for clarity |

### Creator & Strategy Personalities

| Personality | Emoji | Description |
|-------------|:-----:|-------------|
| Book Positioning Strategist | 📚 | Publishing strategy, market positioning, book concepts |
| Creator Business Architect | 🏗️ | Solo creator business modeling and monetization |
| Offer Architect | 💰 | Product offer design and pricing strategy |
| Productivity Architect | ⏱️ | Weekly productivity system design |
| Prompt Engineer | 🎯 | LLM prompt design and optimization |
| Viral Reverse Engineer | 📈 | Social media growth analysis and virality patterns |
| YouTube Niche Strategist | 🎬 | CPM analysis and channel positioning |

---

## 🛠 Skills

Reusable skill modules with YAML frontmatter — drop into your `skills/` directory.

| Skill | Description |
|-------|-------------|
| `git-workflow-optimization` | Branch management, clean commits, PR workflows |
| `testing-debugging` | TDD patterns, test organization, debugging strategies |
| `code-review-checklist` | Systematic review for quality, security, maintainability |
| `docker-local-dev` | Standardized Docker setup for local development |

---

## 📁 Project Structure

```
.claude-plugin/
  plugin.json               # Plugin metadata
agents/                     # 136 Claude Code agent definitions
  biz/                      # Business & product
  core-dev/                 # Core development
  data-ai/                  # Data & AI
  dev-exp/                  # Developer experience
  domains/                  # Specialized domains
  infra/                    # Infrastructure
  lang/                     # Language specialists
  meta/                     # Meta-orchestration
  qa-sec/                   # Quality & security
  research/                 # Research & analysis
  feature-dev/              # Feature development
  code-simplifier/          # Code simplification
  superpowers/              # Code review
skills/                     # Reusable skill modules
personalities/
  general/                  # Framework-agnostic personalities
  claude-code/              # Claude Code-specific (legacy)
docs/                       # Contributing guidelines
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on submitting new agents, personalities, and skills.

**Agents** → `agents/{category}/agent-name.md` with YAML frontmatter (`name`, `description`, `tools`, `model`)

**Personalities** → `personalities/general/personality-name.md` with Description, System Prompt, Use Cases, Metadata

**Skills** → `skills/skill-name/SKILL.md` with YAML frontmatter (`name`, `description`)

---

## 📄 License

MIT — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <em>Built for AI agents, by AI agents.</em> 🐀
</p>
