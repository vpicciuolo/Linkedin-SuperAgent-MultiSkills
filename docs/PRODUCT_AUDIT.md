# Product audit and rebuild decisions

## What the reference category already did well

The strongest open-source LinkedIn skill packs share four good ideas: focused
commands, draft-before-publish behavior, reusable voice guidance, and local
editing tools. Those ideas are worth keeping because they reduce setup and make
the model's behavior easier to predict.

## Gaps found in the reviewed project

The rebuild addresses these gaps:

1. Host lock-in. State paths, commands, and manifests were centered on one AI
   workspace. OYYO uses portable Agent Skills and one neutral state directory.
2. Missing product modes. Research, newsletters, campaigns, employee advocacy,
   evidence management, and reusable strategy were absent or shallow.
3. Fragile claims. Fixed recommendations about reach, timing, links, length,
   and platform behavior can age quickly. OYYO treats them as hypotheses and
   verifies exact limits when they matter.
4. Detector theater. A weighted heuristic score can look scientific while
   penalizing valid formal writing or short copy. OYYO provides transparent
   editorial findings and makes no authorship claim.
5. Unsafe lexical rewriting. Blind word substitution can change meaning. The
   bundled Humanizer uses editorial judgment, and the local linter flags rather
   than rewrites.
6. Thin engineering controls. The reviewed package had no test suite or CI for
   scripts, manifests, cross-platform paths, CSV edge cases, or package shape.
7. Incomplete trust boundaries. Content fetched from a social platform can
   contain prompt injection or private data. OYYO treats all external content
   as untrusted data and separates it from approvals.
8. Weak learning loop. Performance advice was useful but not built around a
   portable schema, missing-data handling, sample-size caveats, or controlled
   experiments.
9. Installation drift. A single marketplace format does not cover the current
   ecosystem. OYYO ships portable, Codex, Claude Code, and manual skill paths.

## Market categories

| Category | Strength | Common weakness | OYYO choice |
| --- | --- | --- | --- |
| Writing-first skill packs | Fast, cheap, easy to inspect | Generic voice, prompt duplication, little measurement | Focused skills plus shared voice, evidence, and state |
| Browser-control agents | Can act on a live account | Account-policy, privacy, and maintenance risk | No unauthorized browser automation |
| API publishing agents | Reliable structured actions | OAuth setup, approval scope, platform access | Optional future integration, separate from the base pack |
| Schedulers and SaaS tools | Team workflows and calendars | Account connection, recurring cost, data leaves device | Local-first core with export-based analytics |
| Humanizers and AI detectors | Easy editorial pass | Semantic damage or misleading detector claims | Humanizer for prose; transparent local lint only |
| General social agents | Broad channel coverage | Shallow LinkedIn-specific reasoning | LinkedIn-focused skills with cross-agent packaging |

## Feature priorities

The highest-value capabilities are not more autonomous clicking. They are
better source material, verified claims, a durable voice profile, a connected
strategy, clear approval boundaries, and a measurement loop that can admit
uncertainty. Those choices make the pack useful to individuals and teams while
keeping the default install free of credentials and external services.

## Current platform facts used in the design

- LinkedIn prohibits unauthorized bots, scraping, and automated engagement:
  https://www.linkedin.com/legal/user-agreement
- LinkedIn's official APIs include member posting through `w_member_social`:
  https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access
- Document upload limits and supported formats can change and should be checked
  before production:
  https://www.linkedin.com/help/linkedin/answer/a564109/media-file-types-supported-on-linkedin
- OpenAI's current plugin format separates manifests, skills, optional tools,
  and onboarding:
  https://developers.openai.com/plugins/build/plugins

This file records product decisions, not legal advice or a promise that current
platform documentation will remain unchanged.
