# Changelog

All notable changes follow Semantic Versioning.

## 2.2.0 - 2026-10-12

- Removed logo artwork and image badges from the README and aligned its
  structure, navigation, ecosystem links, ownership language, and release
  information with the other public repositories maintained by Vincenzo
  Picciuolo.
- Added a complete self-contained Markdown agent for ChatGPT, Claude,
  Perplexity, Gemini, local models, and other file-aware AI workspaces.
- Added compact ChatGPT/web instructions and a detailed cross-platform install
  guide covering local, offline, web, plugin, skill, and hosted-agent use.
- Added a zero-dependency offline installer for all 24 independent skills.
- Added a reproducible distribution builder for the portable Markdown agent
  and single-folder plugin ZIP.
- Added release automation that validates the pack and publishes both portable
  artifacts for every version tag.
- Added distribution and installation tests and expanded pack validation to
  cover the new portable files and scripts.
- Added the project to the `vpicciuolo` profile README.

## 2.1.0 - 2026-10-12

- Added manual, automatic browser-assisted, and official API operating modes.
- Added explicit `read`, `publish`, and `manage` access scopes with a required
  LinkedIn automation risk acknowledgement for automatic mode.
- Added independent automation setup, worker, live account audit, and account
  management skills, bringing the pack to 24 skills.
- Added a zero-dependency worker utility with capability checks, a scoped action
  queue, per-action approvals, cancellations, and append-only completion
  receipts.
- Added local automation and account-snapshot templates without credential
  storage.
- Added workflows for current profiles, recent posts, actual publishing times,
  comments, notifications, inbox triage, company pages, and profile changes.
- Documented official API scope limits and automatic-mode account risk. The pack
  does not add scraping, stealth, CAPTCHA bypass, or bulk engagement automation.

## 2.0.0 - 2026-10-12

- Rebuilt the project as an OYYO ONE AI multi-skill agent pack.
- Added portable Agent Plugin, Codex, and Claude Code manifests.
- Added 20 focused skills covering strategy, writing, engagement, profiles,
  analytics, campaigns, newsletters, repurposing, advocacy, and setup.
- Bundled the MIT-licensed Humanizer skill with its original attribution.
- Added a zero-dependency local CLI for onboarding, content linting, character
  counts, CSV analytics, and workspace initialization.
- Added shared state templates, a 24-pattern hook library, an evidence ledger,
  safety rules, and prompt-injection boundaries.
- Added unit tests, pack validation, and continuous integration.
- Made all LinkedIn actions draft-first and approval-gated. Unauthorized
  scraping or browser automation is outside the supported workflow.
