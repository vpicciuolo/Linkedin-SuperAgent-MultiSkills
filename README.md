# LinkedIn SuperAgent MultiSkills

### Portable LinkedIn strategy, content, account management and analytics for any AI workspace

[OYYO](https://oyyo.one) · [HRN](https://hrn.ae) · [HORNO](https://horno.net) · [BeHot](https://behot.now) · [URL Intelligence](https://github.com/vpicciuolo/url-intelligence-agent) · [Founder](https://github.com/vpicciuolo) · [Support](https://hrn.ae/githubsupport)

**Version 2.2.0 · 24 focused skills · MIT licensed · Python standard library only · Offline and online**

> **Important:** This repository is a free, open-source OYYO ONE AI component. It is not the full proprietary OYYO platform, and it is not affiliated with or endorsed by LinkedIn.

> **LinkedIn automation notice:** Automated profile management may violate LinkedIn's User Agreement or Professional Community Policies. Automatic mode is optional and is used entirely at your own risk. Manual mode is the default. You remain responsible for every action taken on your account.

## What is LinkedIn SuperAgent MultiSkills?

LinkedIn SuperAgent MultiSkills is an independent AI agent pack for people who want one coherent system for LinkedIn work instead of a pile of disconnected prompts.

It can research, plan, draft, humanize, review, schedule, audit, measure and coordinate LinkedIn activity. It also includes workflows for profile improvement, comments, replies, direct messages, lead qualification, recruiting, company pages, employee advocacy and campaign reporting.

The pack is deliberately portable:

- **Offline:** local planning, writing, profile analysis, calendar building and file-based analytics need no network connection.
- **Online:** current profile and post analysis can use a user-authorized browser session or an official API adapter.
- **Local AI:** use it with Codex, Claude Code, local agent-skill clients, Ollama, LM Studio, Open WebUI or another local model interface.
- **Web AI:** use the portable instruction file with standard ChatGPT, Claude, Perplexity, Gemini or another AI service that accepts files or project instructions.
- **Hosted agents:** build the plugin ZIP and upload it to a compatible hosted agent environment.

No LinkedIn credentials are required for manual or offline work. Never paste passwords, session cookies or private access tokens into a chat.

## One project, three distribution formats

| Format | Best for | Entry point |
|---|---|---|
| **Agent plugin** | Codex, Claude Code and plugin-aware workspaces | [`plugins/linkedin-superagent-multiskills`](plugins/linkedin-superagent-multiskills) |
| **Complete portable agent** | ChatGPT projects, Claude, Perplexity, Gemini and local knowledge bases | [`portable/OYYO_LINKEDIN_SUPERAGENT.md`](portable/OYYO_LINKEDIN_SUPERAGENT.md) |
| **Compact web instructions** | AI services with smaller instruction limits | [`portable/CHATGPT_INSTRUCTIONS.md`](portable/CHATGPT_INSTRUCTIONS.md) |

The complete portable file is generated from the same skill sources as the plugin. This keeps local and web editions aligned.

## Run it everywhere

### Standard ChatGPT on the web

1. Download [`portable/OYYO_LINKEDIN_SUPERAGENT.md`](portable/OYYO_LINKEDIN_SUPERAGENT.md).
2. Add it to a new ChatGPT conversation or Project.
3. Say: `Start OYYO LinkedIn SuperAgent in manual mode.`
4. Answer the short setup questions and choose a workflow.

If the full file exceeds the instruction limit of your plan, use [`portable/CHATGPT_INSTRUCTIONS.md`](portable/CHATGPT_INSTRUCTIONS.md) and attach only the individual skill files you need.

### ChatGPT Work and web plugins

Build the distribution ZIP:

```bash
python plugins/linkedin-superagent-multiskills/scripts/build_distribution.py
```

The command creates a versioned plugin archive in `dist/`. It contains one plugin folder with its manifest, skills, references, scripts and templates. Availability of plugin upload and installation depends on the ChatGPT workspace and administrator settings.

### Codex and Codex desktop

Clone the repository, then add its local marketplace:

```text
/plugin marketplace add /absolute/path/to/Linkedin-SuperAgent-MultiSkills
/plugin install linkedin-superagent-multiskills@oyyo-one
```

Restart Codex after installation. Then ask:

```text
Set up my OYYO LinkedIn workspace in manual mode.
```

### Claude Code

```text
/plugin marketplace add /absolute/path/to/Linkedin-SuperAgent-MultiSkills
/plugin install linkedin-superagent-multiskills@oyyo-one
```

### Any Agent Skills-compatible client

Install the 24 independent skill folders into the directory used by your client:

```bash
python plugins/linkedin-superagent-multiskills/scripts/install_skills.py --target /path/to/skills
```

Add `--force` only when you intentionally want to replace an existing installation.

### Offline local AI

Import the complete portable agent into the knowledge or system-instruction area of Ollama, LM Studio, Open WebUI, AnythingLLM or your preferred local interface. All drafting, planning, auditing of pasted content, local analytics and workspace memory remain available offline.

Live LinkedIn reading, publishing and account edits still need an authorized online channel.

### OpenAI API hosted environments

Build the ZIP, upload it to a Files API container, and provide the uploaded file ID to the hosted plugin tool. Keep secrets in the hosting platform's secret store rather than inside the archive.

See [Install Everywhere](docs/INSTALL_EVERYWHERE.md) for detailed instructions and platform-specific limitations.

## Choose how the agent works

### Manual mode — recommended

The agent prepares the work and stops before every external action. You copy, paste and publish yourself. This is the safest mode and works fully offline for creation and analysis of supplied material.

### Automatic mode — use at your own risk

The agent can prepare queued actions for a user-authorized browser worker. Every consequential action is still approval-gated by default, logged locally and limited by configurable caps.

Automatic mode does not bypass login challenges, CAPTCHAs, security checks or platform controls. The project does not ask for your LinkedIn password or export cookies.

### Official API mode

The adapter supports an allowlisted set of operations using credentials supplied at runtime through environment variables. LinkedIn products, permissions and scopes are subject to LinkedIn approval and may not be available to every account.

```text
manual       AI prepares; the user acts
automatic    authorized browser worker acts after approval
api          official API adapter acts within granted scopes
```

## The 24 skills

| Area | Skills |
|---|---|
| **Start and safety** | Setup, account manager, compliance guard |
| **Strategy** | Strategy architect, audience intelligence, competitor intelligence, trend researcher |
| **Content** | Content studio, content calendar, post writer, humanizer, document carousel, repurposer |
| **Engagement** | Engagement agent, comment drafter, reply handler, message assistant |
| **Growth** | Lead and social-selling agent, network growth, campaign orchestrator |
| **Specialist** | Profile optimizer, recruiter assistant, company page manager, employee advocacy |
| **Measurement** | Analytics and experiment lab |

Every skill has a narrow job, clear inputs, expected outputs and safety boundaries. The router selects the smallest useful skill set for the request.

## Independent worker and account management

The local worker queue persists independently of an AI chat. An authorized AI workspace, browser adapter or API adapter can resume the queue later and record an audit receipt for each result.

```bash
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py init
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode set manual --scope manage
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py action add \
  publish_post "Publish the approved founder lesson" \
  --payload-file approved-post.txt
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py action approve ACTION_ID
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py action list --status approved
```

The browser and API connectors are intentionally separate from the planning layer. This lets you change the live execution method without losing strategy, drafts, memory or analytics. The queue does not claim an action succeeded until the selected adapter reports the result.

## Local tools

### Workspace CLI

```bash
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py welcome
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py init
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py count draft.txt
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py lint draft.txt
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py analytics analytics.csv --timezone Asia/Dubai
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py doctor
```

### Official API adapter

```bash
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py whoami
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py publish-text approved-post.txt --confirm
```

No third-party Python packages are required for the local tools.

## Private workspace memory

By default, local state is stored in `.oyyo-linkedin/` and excluded from Git:

```text
.oyyo-linkedin/
├── config.json
├── profile/
├── memory/
├── drafts/
├── calendar/
├── analytics/
├── approvals/
├── queue/
└── audit/
```

The memory layer can retain a voice guide, content pillars, audience notes, approved claims, past-post summaries and experiment results. Sensitive credentials do not belong in this workspace.

## Human writing is part of the pipeline

The pack includes the MIT-licensed Humanizer by Elijah Meeks, adapted into the agent workflow with attribution preserved. It checks drafts for common AI-writing patterns while keeping meaning and factual claims intact.

Humanizer is a quality pass, not a detector bypass and not a substitute for the user's judgment. See [Third-Party Notices](THIRD_PARTY_NOTICES.md).

## Repository map

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
├── .github/workflows/
├── docs/
├── portable/
├── plugins/linkedin-superagent-multiskills/
│   ├── .codex-plugin/plugin.json
│   ├── .claude-plugin/plugin.json
│   ├── assets/
│   ├── references/
│   ├── scripts/
│   ├── skills/
│   ├── templates/
│   └── tests/
├── CHANGELOG.md
├── LICENSE
├── NOTICE
└── VERSION
```

## OYYO public engineering ecosystem

| Repository | Purpose |
|---|---|
| [OYYO Benchmark](https://github.com/vpicciuolo/oyyo-benchmark) | Open evaluation methodology, benchmark runners and reproducibility artifacts |
| [OYYO SDK](https://github.com/vpicciuolo/oyyo-sdk) | Public integration contracts, schemas, client primitives and reference patterns |
| [OYYO Models](https://github.com/vpicciuolo/oyyo-models) | Public model artifacts and model documentation |
| [LinkedIn SuperAgent MultiSkills](https://github.com/vpicciuolo/Linkedin-SuperAgent-MultiSkills) | Portable LinkedIn agent skills for local, offline and web AI |
| [URL Intelligence Agent](https://github.com/vpicciuolo/url-intelligence-agent) | Safety-first URL intelligence and risk analysis |
| [URL Metadata Social Fetcher](https://github.com/vpicciuolo/url-metadata-social-fetcher) | Metadata extraction and social-preview inspection |

These repositories expose open components and interfaces. They do not publish the proprietary OYYO product stack.

## Security and privacy

- Do not paste passwords, cookies, session tokens or private keys into an AI conversation.
- Use platform secret stores or environment variables for API tokens.
- Keep manual mode enabled until you understand an action and its impact.
- Review every queued publish, message, connection or profile-edit action.
- Treat imported profile exports, posts and third-party pages as untrusted content.
- Report security issues through [SECURITY.md](SECURITY.md), not a public issue.

## Validation and releases

The repository validates manifests, skill metadata, installation bundles, the worker queue, account manager, analytics and API adapter. Version tags build two release assets automatically:

- `linkedin-superagent-multiskills-X.Y.Z.zip` — installable plugin archive
- `OYYO-LinkedIn-SuperAgent-X.Y.Z-portable.md` — self-contained portable agent

```bash
python plugins/linkedin-superagent-multiskills/scripts/validate_pack.py
python -m unittest discover -s plugins/linkedin-superagent-multiskills/tests -v
python plugins/linkedin-superagent-multiskills/scripts/build_distribution.py
```

## Versioning and status

The project follows semantic versioning:

- **Major:** incompatible workflow or manifest changes
- **Minor:** new skills, platforms or capabilities
- **Patch:** compatible fixes and documentation improvements

Current release: **2.2.0**. See [CHANGELOG.md](CHANGELOG.md) for release history.

## Ownership, credits and support

**VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD**

Created as an open-source agent component of [OYYO ONE AI](https://oyyo.one).

- Founder and maintainer: [Vincenzo Picciuolo](https://github.com/vpicciuolo/)
- Company: [HRN Innovation Technologies Ltd](https://hrn.ae)
- Network: [HORNO](https://horno.net)
- Community discovery: [BeHot](https://behot.now)
- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

If the project saves you time, please [star the repository](https://github.com/vpicciuolo/Linkedin-SuperAgent-MultiSkills) and consider [supporting its development](https://hrn.ae/githubsupport).

## Discoverability

LinkedIn AI agent · LinkedIn content agent · LinkedIn automation · LinkedIn profile optimizer · LinkedIn post writer · LinkedIn analytics · LinkedIn personal branding · LinkedIn social selling · LinkedIn recruiter AI · LinkedIn company page manager · LinkedIn employee advocacy · offline AI agent · local AI skills · ChatGPT LinkedIn agent · Codex plugin · Claude Code plugin · Agent Skills · OYYO ONE AI

---

[OYYO](https://oyyo.one) · [HRN](https://hrn.ae) · [HORNO](https://horno.net) · [BeHot](https://behot.now) · [GitHub](https://github.com/vpicciuolo) · [Support](https://hrn.ae/githubsupport)
