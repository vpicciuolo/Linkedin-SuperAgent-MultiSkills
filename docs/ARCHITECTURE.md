# Architecture

## Design goals

The pack is portable, draft-first, local-first, testable, and safe to extend.
It separates instructions that require judgment from deterministic local tools.

## Layers

1. Marketplace manifests make the package discoverable in Codex and Claude
   Code.
2. The portable plugin manifest identifies the package for Agent Plugin hosts.
3. Focused skills handle recognizable user goals and disclose detailed
   instructions only when selected.
4. Shared references define truth, safety, state, hooks, profile scoring, and
   analytics semantics once.
5. Templates give every supported host the same local memory structure.
6. The Python utility handles deterministic counting, linting, initialization,
   and CSV calculations without network access.

## Routing

`oyyo-linkedin` is the broad router. A narrow request should invoke the focused
skill directly. Multi-step work moves through foundation, planning, production,
approval, and learning, but the user can enter at any point.

## State

`.oyyo-linkedin/` is project-local and Git-ignored. The user controls whether
anything is created or saved. `OYYO_LINKEDIN_HOME` can point to a deliberate
shared location.

Skills read only the state relevant to the task. New evidence supplements
rather than silently replaces the user's declared voice, strategy, or limits.

## Permission model

Drafting, analysis, and local file generation do not require an account
connection. Publishing, scheduling, sending, reacting, connecting, or editing
a live profile is a separate external action and requires explicit approval at
the time of the action.

The base pack contains no live connector. A future integration should use an
official or otherwise authorized interface, declare its permissions, keep
tokens outside the repository, and preserve the per-action approval gate.

## Extension points

- Add a skill when a user goal has a distinct trigger, input, and output.
- Add a reference when several skills need the same maintained knowledge.
- Add a script only for repeatable deterministic work.
- Add an MCP or app connection only when live data or external action is
  essential and the integration can be authorized safely.

Keep plugin version, `VERSION`, changelog, tests, and skill metadata aligned.
