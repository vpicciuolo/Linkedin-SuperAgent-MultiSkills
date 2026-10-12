# Local workspace state

Use `.oyyo-linkedin/` in the current project by default. If the environment
variable `OYYO_LINKEDIN_HOME` is set, use that directory instead. Create state
only when the user asks to save, initialize, log, or maintain it.

## Files

| File | Purpose |
| --- | --- |
| `profile.md` | identity, offer, audience, goals, boundaries |
| `voice.md` | observed voice rules with quoted examples |
| `story-bank.md` | true stories, decisions, mistakes, proof, lessons |
| `strategy.md` | positioning, pillars, formats, cadence, experiments |
| `calendar.md` | current content plan |
| `content-log.csv` | published content and later performance |
| `evidence-ledger.csv` | externally sourced claims used in drafts |

Never silently overwrite user edits. Merge new observations, preserve a dated
note for disputed guidance, and ask before replacing a declared position or
off-limits topic.

`content-log.csv` uses these columns:

```text
published_at,title_or_hook,format,pillar,goal,impressions,reactions,comments,reposts,saves,sends,profile_views,follows,leads,notes
```

The numeric performance fields may be blank. Do not turn blanks into zero
unless the export explicitly reports zero.
