# Install and use everywhere

The project has three distribution forms:

1. the full plugin under `plugins/linkedin-superagent-multiskills/`;
2. a compact instruction file at `portable/CHATGPT_INSTRUCTIONS.md`;
3. a generated complete portable Markdown file containing all skills and shared
   references.

Writing, planning, profile work, audits from supplied files, and local analytics
can run offline. Live research and account actions need browser or API tools from
the selected AI host.

## Standard ChatGPT web chat

This is the simplest route for standard ChatGPT web, sometimes called classic
ChatGPT:

1. Download `portable/CHATGPT_INSTRUCTIONS.md` for compact use, or generate and
   download the complete portable bundle.
2. Attach the file to a chat, Project, or custom GPT when that feature is
   available. Ask ChatGPT to follow it as the operating instructions for the
   conversation.
3. If file upload or persistent instructions are unavailable, copy the compact
   file into the conversation before the first LinkedIn request.

Manual mode works immediately. A normal web chat cannot perform browser or API
actions unless the selected ChatGPT surface has a suitable tool or connected
service.

## ChatGPT Work and ChatGPT web Plugins

The repository is ready as a skills-only Agent Plugin. A workspace admin can
publish a tested local plugin inside the workspace. Public one-click discovery
requires submission, review, and publication in the universal Plugins
Directory shared by ChatGPT and Codex.

The repository and its GitHub release do not by themselves create a public
directory listing. Until the listing is approved, use the portable bundle on
the web or the repo marketplace in supported local clients.

## Codex and ChatGPT desktop

```text
codex plugin marketplace add vpicciuolo/Linkedin-SuperAgent-MultiSkills
```

Restart the client, open the Plugins Directory, choose `OYYO ONE Open Source`,
and install `OYYO LinkedIn SuperAgent`.

## Claude Code

```text
/plugin marketplace add vpicciuolo/Linkedin-SuperAgent-MultiSkills
/plugin install linkedin-superagent-multiskills@oyyo-one-open-source
```

Restart the session and invoke `oyyo-linkedin-setup`.

## Any Agent Skills client

When Node.js and internet access are available:

```bash
npx skills add ./plugins/linkedin-superagent-multiskills --global --agent '*'
```

For a fully offline install, copy the skills into the directory used by the
local agent:

```bash
python plugins/linkedin-superagent-multiskills/scripts/install_skills.py --target /path/to/agent/skills
```

The installer does not guess private configuration paths and does not overwrite
existing skills unless `--force` is supplied.

## Offline local AI

The complete portable Markdown file works as a system prompt or knowledge file
in local tools such as Ollama frontends, LM Studio, Open WebUI, AnythingLLM, and
other software that accepts instructions or uploaded text files.

Build it without internet access or third-party Python packages:

```bash
python plugins/linkedin-superagent-multiskills/scripts/build_distribution.py
```

The command creates:

```text
dist/OYYO-LinkedIn-SuperAgent-<version>-portable.md
dist/linkedin-superagent-multiskills-<version>.zip
```

Use the portable Markdown file when the host does not support Agent Skills. Use
the ZIP when the host accepts an Agent Plugin package.

## Claude web, Perplexity, Gemini, and other web AI

Upload the complete portable Markdown file as project knowledge or attach it to
the conversation. When the product has no file upload, paste the compact
instructions. Product capabilities differ, so manual mode is always the
fallback. Browser and API actions require tools supplied and authorized by that
product.

## OpenAI API hosted environments

Build the plugin ZIP and supply it as a plugin package to an OpenAI-hosted
environment that supports uploaded plugins. The ZIP contains one top-level
plugin folder and its `.codex-plugin/plugin.json` manifest.

## Offline capability boundary

Offline use includes drafting, editing, strategy, voice matching, story-bank
work, content calendars, profile rewrites, analytics from local CSV files,
action queues, and Humanizer. It cannot verify current news, inspect a live
LinkedIn account, or publish until a browser or official API adapter is added.
