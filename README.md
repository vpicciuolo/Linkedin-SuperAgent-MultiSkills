<p align="center">
  <img src="plugins/linkedin-superagent-multiskills/assets/logo.svg" alt="OYYO ONE AI LinkedIn SuperAgent MultiSkills" width="820">
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-00C2A8.svg"></a>
  <a href="VERSION"><img alt="Version 2.1.0" src="https://img.shields.io/badge/version-2.1.0-6D5EF7.svg"></a>
  <img alt="24 agent skills" src="https://img.shields.io/badge/agent_skills-24-0B1020.svg">
  <img alt="Python standard library only" src="https://img.shields.io/badge/runtime-zero_dependencies-FFCD4A.svg">
</p>

# Linkedin-SuperAgent-MultiSkills

OYYO LinkedIn SuperAgent is a free, open-source LinkedIn AI agent for strategy,
content, live audits, profile management, engagement, campaigns, and analytics.
It can work manually, through a user-authorized browser session, or through
LinkedIn's official APIs when the required products and scopes are available.

It works as a plugin in Codex and Claude Code, and as a standard skill pack in
other compatible AI workspaces. Manual mode needs no LinkedIn login, API key,
SaaS account, or telemetry connection. Live modes keep credentials in the
user's browser, host secret store, or environment rather than the project.

Created by [Vincenzo Picciuolo](https://github.com/vpicciuolo/) © 2026
[HRN Innovation Technologies Ltd](https://hrn.ae), as part of
[OYYO ONE AI](https://oyyo.one).

## What is inside

The pack has 24 focused skills. The router selects one when the request spans
several workflows; every skill can also run directly.

| Group | Skills | What they do |
| --- | --- | --- |
| Start | `oyyo-linkedin`, `oyyo-linkedin-setup`, `linkedin-automation-setup` | Route work, initialize private local state, choose manual, automatic, or API mode |
| Operations | `linkedin-worker`, `linkedin-live-audit`, `linkedin-account-manager` | Run a queue, inspect the current account and recent posts, manage approved changes |
| Foundation | `linkedin-voice-lab`, `linkedin-story-bank`, `linkedin-strategy` | Learn the user's voice, collect true material, define audience and positioning |
| Planning | `linkedin-content-plan`, `linkedin-research`, `linkedin-campaign` | Build calendars, source current claims, coordinate launches and events |
| Writing | `linkedin-hook-lab`, `linkedin-post-writer`, `linkedin-carousel`, `linkedin-newsletter`, `linkedin-repurposer` | Create native posts, document posts, long-form issues, and multi-format adaptations |
| Engagement | `linkedin-comment`, `linkedin-reply`, `linkedin-dm` | Add useful comments, handle threads, and write ethical one-to-one outreach |
| Growth operations | `linkedin-profile`, `linkedin-analytics`, `linkedin-employee-advocacy` | Improve profiles, learn from exports, and run voluntary team programs |
| Editorial | `humanizer` | Remove common AI writing patterns without changing the facts |

## Why this version is different

- Cross-agent packaging. Portable Agent Plugin, Codex, Claude Code, and plain
  Agent Skills layouts ship together.
- One local memory model. Voice, stories, strategy, calendar, evidence, and
  content history live in `.oyyo-linkedin/`, not in a vendor-specific folder.
- Truth before polish. Missing facts remain visible as `{{NEEDS INPUT}}`
  markers, which block the pre-publish check.
- Three operating modes. Choose manual guidance, browser-assisted automatic
  work, or approved official API operations without changing skills.
- Worker-grade control. Access scopes, action queues, per-action approvals,
  completion receipts, and capability checks keep multi-step work inspectable.
- Current-account audits. Review the live profile, recent posts, publishing
  times, comments, notifications, and analytics available in the selected mode.
- Evidence-aware research. Current claims use an evidence ledger with source,
  date, scope, and caveat.
- Useful analytics. The local tool reads common CSV column names, preserves
  missing values, compares normalized rates, and labels small samples.
- No fake detector promise. Humanizer is an editorial tool. The local linter
  checks concrete writing risks and never claims to prove authorship.
- Maintainer-ready. Semantic versioning, CI, validation, unit tests, security
  guidance, and third-party notices are included.

## Quick start

### Install in Claude Code

Run these inside Claude Code:

```text
/plugin marketplace add vpicciuolo/Linkedin-SuperAgent-MultiSkills
/plugin install linkedin-superagent-multiskills@oyyo-one-open-source
```

Restart the session, then ask:

```text
Use oyyo-linkedin-setup to initialize my LinkedIn workspace.
```

### Install in Codex

Add the repository as a plugin marketplace:

```text
codex plugin marketplace add vpicciuolo/Linkedin-SuperAgent-MultiSkills
```

Restart Codex, open the Plugins Directory, choose **OYYO ONE Open Source**, and
install **OYYO LinkedIn SuperAgent**. You can then invoke `$oyyo-linkedin` or
ask for a LinkedIn task in plain language.

The repository also contains the portable Agent Plugin manifest described in
the current [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

### Install in multiple Agent Skills clients

Clone the repository, then let the Skills CLI install the package for the
agents it recognizes:

```bash
git clone https://github.com/vpicciuolo/Linkedin-SuperAgent-MultiSkills.git
cd Linkedin-SuperAgent-MultiSkills
npx skills add ./plugins/linkedin-superagent-multiskills --global --agent '*'
```

Leave off `--global` for a project-only install. This route is useful for
Codex, Claude Code, Cursor, Gemini CLI, GitHub Copilot, Windsurf, and other
clients supported by the Skills CLI.

### Use it in a chat-only workspace

If a workspace does not support Agent Skills, paste
`plugins/linkedin-superagent-multiskills/skills/oyyo-linkedin/SKILL.md` into
project instructions and add the focused skill needed for the task. Writing
workflows still function, but local scripts and automatic skill routing may
not be available.

Do not assume that every product branded as an AI workspace supports plugins
or filesystem tools. Use the manual method when native skills are unavailable.

## Choose how the agent works

The same 24 skills work in all three modes.

| Mode | Best for | Account access | Main limit |
| --- | --- | --- | --- |
| Manual | safest setup and any unsupported client | no stored connection; user copies, pastes, and clicks | user performs live changes |
| Automatic | broad profile, content, page, inbox, and engagement workflows in a browser-capable AI workspace | user signs in directly and grants `read`, `publish`, or `manage` scope | LinkedIn does not permit third-party browser automation; account restriction risk |
| API | approved posting and account operations through LinkedIn OAuth | official token in the host secret store or environment | actions are limited to products and scopes approved for the app |

Use setup in plain language:

```text
Use linkedin-automation-setup. Configure manual mode with manage scope.
```

```text
Use linkedin-automation-setup. Show me the risk warning, then configure automatic mode with manage scope.
```

```text
Use linkedin-automation-setup. Check my official LinkedIn API products and configure only the actions my scopes support.
```

### Required automatic-mode warning

> **LinkedIn automation warning:** LinkedIn states that it does not permit
> third-party software or browser extensions that scrape, modify, or automate
> activity on its website. Automated profile management and other browser-based
> activity may violate LinkedIn's User Agreement and can lead to account
> restrictions. Automatic mode is optional and is used at your own risk.

The project does not include stealth, CAPTCHA bypass, fingerprint masking,
cookie collection, scraping, fake engagement, or bulk spam. The user signs in
directly. A `manage` scope lets the worker prepare all supported work, but every
publish, send, connection, profile edit, page edit, and deletion still needs a
clear approval immediately before it happens.

## Start here

```text
Use linkedin-voice-lab. Learn my voice from these five posts and show the evidence for each rule.
```

```text
Use linkedin-story-bank. Interview me about the last two weeks and find five truthful post ideas.
```

```text
Use linkedin-strategy. Build a 30-day plan for reaching UAE hospitality founders without generic AI content.
```

```text
Use linkedin-post-writer. Turn this result into a post for operations leaders. Do not invent any numbers.
```

```text
Use linkedin-analytics. Analyze this export, explain the missing data, and propose two tests for next month.
```

```text
Use linkedin-live-audit in my selected mode. Review my profile, last 30 posts, actual posting times, unanswered comments, and three next experiments.
```

```text
Use linkedin-worker. Build a queue to refresh my profile, prepare this week's posts, and handle meaningful replies. Do not execute writes until I approve each one.
```

More examples are in [the prompt cookbook](docs/PROMPT_COOKBOOK.md).

## Local tools

The local content and worker utilities use only the Python standard library and
make no network calls. `linkedin_api.py` is an optional official API adapter;
it makes a network call only when the user runs a specific command.

```bash
# Show the project credit and support links
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py welcome

# Create .oyyo-linkedin/ without overwriting existing files
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py init

# Count a draft
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py count draft.txt

# Run the pre-publish editorial check
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py lint draft.txt

# Analyze an exported CSV and normalize aware timestamps to Dubai time
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py analytics analytics.csv --timezone Asia/Dubai

# Show or select an operating mode
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode show
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode set manual --scope manage
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode set api --scope publish --api-scope openid --api-scope w_member_social

# Verify the chosen adapter without printing secret values
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py doctor

# Queue and approve a live action
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py action add publish_post "Publish approved launch post"
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py action approve <action-id>

# API mode: verify identity, then publish only after the queued action is approved
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py whoami
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py publish-text approved-post.txt --confirm
```

Use `--json` with `count`, `lint`, `init`, or `analytics` when another tool
needs structured output. The API adapter requires `LINKEDIN_ACCESS_TOKEN`,
`LINKEDIN_ACTOR_URN`, and `LINKEDIN_VERSION` in the environment. Never put
their values in the repository or a prompt.

## The local workspace

Initialization creates:

```text
.oyyo-linkedin/
├── profile.md
├── voice.md
├── story-bank.md
├── strategy.md
├── calendar.md
├── content-log.csv
├── evidence-ledger.csv
├── automation.json
├── account-snapshot.json
├── action-queue.json          # created when needed
└── action-receipts.jsonl      # created when needed
```

The directory is ignored by Git by default. It must never contain passwords,
session cookies, access tokens, refresh tokens, one-time codes, private-message
archives, or data the user has no right to store.

Set `OYYO_LINKEDIN_HOME` when several projects should use a deliberately shared
workspace. The skills do not create or change that directory unless asked.

## A complete workflow

1. Run setup, create local state, and choose manual, automatic, or API mode.
2. Run a live audit or import the profile, recent posts, and analytics available.
3. Build a voice profile and story bank from real material.
4. Define audience, positioning, pillars, capacity, and measurement.
5. Plan a week or month, then research current claims and record evidence.
6. Draft one asset at a time, then run Humanizer and the local linter.
7. Queue the final action and approve its exact content and target.
8. Execute through the chosen mode and record the live result as a receipt.
9. Analyze actual post times and normalized results before the next experiment.

The pack works for a one-off task too. You can skip setup and ask for a single
comment, profile section, or post.

## Humanizer included

The pack includes the MIT-licensed
[Humanizer](https://github.com/blader/humanizer) skill. It edits common AI
writing patterns while preserving meaning. Its original license is kept in the
skill folder, and the repository records the attribution in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Humanizer does not guarantee that a detector will label text as human. No
editing method can prove who wrote a passage. Use it to make the writing more
specific, natural, and faithful to the user's voice.

## Safety and LinkedIn policy

[LinkedIn says](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin)
it does not permit third-party software or browser extensions that scrape,
change, or automate activity on its website. Automatic mode is an explicit,
opt-in browser workflow with an account-restriction risk. Use it at your own
risk. The project does not include a browser driver, cookie collector, stealth
mode, CAPTCHA bypass, scraper, or engagement bot.

[LinkedIn provides official APIs](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
for approved applications, including member social publishing permissions. API
mode uses only the products and scopes the app has actually received. Official
API access does not equal full website access, and general member-profile
editing is not promised. Unsupported work falls back to manual mode, or to
automatic mode after the warning is accepted.

Read [SECURITY.md](SECURITY.md) and the pack's
[session and safety policy](plugins/linkedin-superagent-multiskills/references/session-and-safety.md)
before adding any live integration. The detailed
[automation modes guide](docs/AUTOMATION_MODES.md) maps profile, content,
engagement, inbox, page, and analytics capabilities across all three modes.

## Architecture

```text
Linkedin-SuperAgent-MultiSkills/
├── .agents/plugins/marketplace.json       # Codex repo marketplace
├── .claude-plugin/marketplace.json        # Claude Code marketplace
├── plugins/linkedin-superagent-multiskills/
│   ├── plugin.json                        # portable Agent Plugin
│   ├── .codex-plugin/plugin.json          # Codex compatibility manifest
│   ├── .claude-plugin/plugin.json         # Claude Code manifest
│   ├── skills/                             # 24 independent focused skills
│   ├── references/                         # shared policy and methods
│   ├── templates/                          # local state templates
│   ├── scripts/                            # zero-dependency local tools
│   ├── tests/                              # unit and package tests
│   └── assets/                             # OYYO visual identity
├── docs/
├── LICENSE
├── THIRD_PARTY_NOTICES.md
└── VERSION
```

The [architecture notes](docs/ARCHITECTURE.md) explain routing, state,
permissions, and extension points. The [product audit](docs/PRODUCT_AUDIT.md)
records what the rebuild fixed and which tradeoffs were chosen.

## Validate a contribution

```bash
python plugins/linkedin-superagent-multiskills/scripts/validate_pack.py
python -m unittest discover -s plugins/linkedin-superagent-multiskills/tests -v
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Versioning

This project uses Semantic Versioning.

- Major: skill behavior, state schema, or compatibility breaks.
- Minor: new skills or backward-compatible capabilities.
- Patch: fixes, wording corrections, tests, and documentation.

The current release is `2.1.0`. See [CHANGELOG.md](CHANGELOG.md).

## Credits, star, and support

**VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD**

- GitHub: [github.com/vpicciuolo](https://github.com/vpicciuolo/)
- HRN Innovation Technologies: [hrn.ae](https://hrn.ae)
- OYYO ONE AI: [oyyo.one](https://oyyo.one)
- Star the project: [Linkedin-SuperAgent-MultiSkills](https://github.com/vpicciuolo/Linkedin-SuperAgent-MultiSkills)
- Support open-source development: [hrn.ae/githubsupport](https://hrn.ae/githubsupport)

The project is free to use, modify, and distribute under the
[MIT License](LICENSE).

## Search keywords

LinkedIn AI agent, LinkedIn content agent, LinkedIn Agent Skills, LinkedIn
automation, LinkedIn browser agent, LinkedIn API agent, LinkedIn account
manager, LinkedIn post writer, LinkedIn humanizer, LinkedIn profile optimizer,
LinkedIn live audit, LinkedIn post timing, LinkedIn carousel generator,
LinkedIn analytics tool,
LinkedIn personal branding, LinkedIn content strategy, LinkedIn comment
writer, LinkedIn DM writer, employee advocacy, founder content, creator
workflow, Codex plugin, Claude Code plugin, Agent Skills, OYYO ONE AI,
open-source LinkedIn tool, MIT LinkedIn agent.
