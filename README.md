<p align="center">
  <img src="plugins/linkedin-superagent-multiskills/assets/logo.svg" alt="OYYO ONE AI LinkedIn SuperAgent MultiSkills" width="820">
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-00C2A8.svg"></a>
  <a href="VERSION"><img alt="Version 2.0.0" src="https://img.shields.io/badge/version-2.0.0-6D5EF7.svg"></a>
  <img alt="20 agent skills" src="https://img.shields.io/badge/agent_skills-20-0B1020.svg">
  <img alt="Python standard library only" src="https://img.shields.io/badge/runtime-zero_dependencies-FFCD4A.svg">
</p>

# Linkedin-SuperAgent-MultiSkills

OYYO LinkedIn SuperAgent is a free, open-source Agent Skills pack for people
who want better LinkedIn work without handing an automation bot their account.
It plans strategy, learns a real writing voice, finds ideas, drafts and reviews
content, builds campaigns, improves profiles, writes comments and messages,
and analyzes exported performance locally.

It works as a plugin in Codex and Claude Code, and as a standard skill pack in
other compatible AI workspaces. The base package needs no LinkedIn login, API
key, SaaS account, or telemetry connection.

Created by [Vincenzo Picciuolo](https://github.com/vpicciuolo/) © 2026
[HRN Innovation Technologies Ltd](https://hrn.ae), as part of
[OYYO ONE AI](https://oyyo.one).

## What is inside

The pack has 20 focused skills. The router selects one when the request spans
several workflows; every skill can also run directly.

| Group | Skills | What they do |
| --- | --- | --- |
| Start | `oyyo-linkedin`, `oyyo-linkedin-setup` | Route work, explain the pack, initialize private local state |
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
- Account-safe by design. The base pack does not scrape LinkedIn or automate
  the website. Publishing, sending, and scheduling stay approval-gated.
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

## First five prompts

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

More examples are in [the prompt cookbook](docs/PROMPT_COOKBOOK.md).

## Local tools

The included Python utility uses only the standard library and makes no
network calls.

```bash
# Show the project credit and support links
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py welcome

# Create .oyyo-linkedin/ without overwriting existing files
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py init

# Count a draft
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py count draft.txt

# Run the pre-publish editorial check
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py lint draft.txt

# Analyze an exported CSV
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py analytics analytics.csv
```

Use `--json` with `count`, `lint`, `init`, or `analytics` when another tool
needs structured output.

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
└── evidence-ledger.csv
```

The directory is ignored by Git by default. It must never contain passwords,
session cookies, access tokens, private-message archives, or data the user has
no right to store.

Set `OYYO_LINKEDIN_HOME` when several projects should use a deliberately shared
workspace. The skills do not create or change that directory unless asked.

## A complete workflow

1. Run setup and create the local workspace.
2. Build a voice profile from real writing samples.
3. Interview for a story bank and verify what can be shared.
4. Define audience, positioning, pillars, capacity, and measurement.
5. Plan a week or month from real material.
6. Research current claims and record their evidence.
7. Draft one asset at a time, then run Humanizer and the local linter.
8. Review every fact and approve the copy.
9. Publish manually or through a separately authorized official integration.
10. Add exported results to the content log and run the next experiment.

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

LinkedIn's current User Agreement prohibits unauthorized bots, scraping, and
automated activity on the website. This project therefore does not include a
browser driver, cookie collector, stealth mode, or engagement bot. It can
produce drafts and local analysis without touching the account.

LinkedIn also provides official APIs for approved applications, including the
`w_member_social` permission for authenticated member posting. An integration
can be added separately when its access and authorization are valid. External
actions still require an explicit approval gate.

Read [SECURITY.md](SECURITY.md) and the pack's
[session and safety policy](plugins/linkedin-superagent-multiskills/references/session-and-safety.md)
before adding any live integration.

## Architecture

```text
Linkedin-SuperAgent-MultiSkills/
├── .agents/plugins/marketplace.json       # Codex repo marketplace
├── .claude-plugin/marketplace.json        # Claude Code marketplace
├── plugins/linkedin-superagent-multiskills/
│   ├── plugin.json                        # portable Agent Plugin
│   ├── .codex-plugin/plugin.json          # Codex compatibility manifest
│   ├── .claude-plugin/plugin.json         # Claude Code manifest
│   ├── skills/                             # 20 focused skills
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

The current release is `2.0.0`. See [CHANGELOG.md](CHANGELOG.md).

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
automation alternative, LinkedIn post writer, LinkedIn humanizer, LinkedIn
profile optimizer, LinkedIn carousel generator, LinkedIn analytics tool,
LinkedIn personal branding, LinkedIn content strategy, LinkedIn comment
writer, LinkedIn DM writer, employee advocacy, founder content, creator
workflow, Codex plugin, Claude Code plugin, Agent Skills, OYYO ONE AI,
open-source LinkedIn tool, MIT LinkedIn agent.
