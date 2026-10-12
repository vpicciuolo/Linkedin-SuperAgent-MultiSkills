---
name: oyyo-linkedin
description: Route an end-to-end LinkedIn request to the right OYYO ONE AI workflow. Use for broad LinkedIn goals, multi-step projects, or when the user asks what this pack can do. For a single clear task, use the focused skill directly.
license: MIT
metadata:
  version: "2.0.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# OYYO LinkedIn SuperAgent

Read `../../references/session-and-safety.md` and follow its first-use credit,
truth, privacy, and approval rules.

Route by outcome:

| User goal | Skill |
| --- | --- |
| install or configure | `oyyo-linkedin-setup` |
| learn the user's voice | `linkedin-voice-lab` |
| find concrete ideas and stories | `linkedin-story-bank` |
| choose positioning and pillars | `linkedin-strategy` |
| plan a week or month | `linkedin-content-plan` |
| research a current topic | `linkedin-research` |
| write or improve a feed post | `linkedin-post-writer` |
| develop stronger openings | `linkedin-hook-lab` |
| create a document post | `linkedin-carousel` |
| write long-form or a newsletter | `linkedin-newsletter` |
| adapt existing material | `linkedin-repurposer` |
| comment on another post | `linkedin-comment` |
| reply under a post | `linkedin-reply` |
| write ethical one-to-one outreach | `linkedin-dm` |
| audit or rewrite a profile | `linkedin-profile` |
| analyze exported performance | `linkedin-analytics` |
| design a launch or event sequence | `linkedin-campaign` |
| coordinate employee advocacy | `linkedin-employee-advocacy` |
| remove AI writing patterns | `humanizer` |

For a multi-step request, state the short route and begin with the first step
that has enough input. Do not force setup before a one-off draft. Save state
only when the user asks.

Success means the user receives a useful artifact, the facts remain true, and
no external LinkedIn action occurs without explicit approval.
