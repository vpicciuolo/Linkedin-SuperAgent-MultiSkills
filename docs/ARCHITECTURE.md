# Architecture

## Design goals

The pack is portable, local-first, mode-aware, testable, and safe to extend. It
separates instructions that require judgment, adapter-specific live actions,
and deterministic local tools.

## Layers

1. Marketplace manifests make the package discoverable in Codex and Claude
   Code.
2. The portable plugin manifest identifies the package for Agent Plugin hosts.
3. Focused skills handle recognizable user goals and disclose detailed
   instructions only when selected.
4. Shared references define truth, safety, operating modes, state, hooks,
   profile scoring, and analytics semantics once.
5. Templates give every supported host the same local memory structure.
6. The content utility handles deterministic counting, linting, initialization,
   and CSV calculations without network access.
7. The worker utility stores the selected mode, validates scope, queues actions,
   records approvals, and writes completion receipts without executing network
   or browser operations itself.

## Routing

`oyyo-linkedin` is the broad router. A narrow request should invoke the focused
skill directly. Multi-step work moves through foundation, planning, production,
approval, and learning, but the user can enter at any point.

`linkedin-worker` owns multi-action sessions. It routes each queue item to a
focused skill, then hands the resulting action to the selected adapter. Every
focused skill remains directly usable and reads the shared mode policy through
`session-and-safety.md`.

## State

`.oyyo-linkedin/` is project-local and Git-ignored. The user controls whether
anything is created or saved. `OYYO_LINKEDIN_HOME` can point to a deliberate
shared location.

Skills read only the state relevant to the task. New evidence supplements
rather than silently replaces the user's declared voice, strategy, or limits.

`automation.json` contains mode, scope, environment-variable names, and approval
policy. It contains no tokens. `action-queue.json` records work in progress and
`action-receipts.jsonl` records final outcomes. These files are local and
Git-ignored with the rest of the workspace.

## Permission model

The user selects an adapter and an access ceiling:

| Adapter | Live surface | Capability source |
| --- | --- | --- |
| manual | none | user performs the UI action |
| automatic | signed-in LinkedIn website | host browser or computer-use tools |
| API | official LinkedIn endpoints | approved app products and OAuth scopes |

Scopes are `read`, `publish`, and `manage`. Publishing, scheduling, sending,
reacting, connecting, deleting, or editing live data requires explicit approval
at the time of the action even under `manage`.

Automatic mode is opt-in and requires the documented LinkedIn risk warning.
The user signs in directly; the pack never collects credentials or browser
state. API mode declares its scope limits and uses environment variables or a
host secret store. Unsupported API operations fall back to manual mode.

## Worker state machine

Read-only actions enter `ready`. Write actions enter `pending_approval` and can
move to `approved`. An adapter can finish only `ready` or `approved` work as
`succeeded` or `failed`. A pending item can become `cancelled`. Final states are
written as receipts so a worker does not confuse a draft with a live change.

## Extension points

- Add a skill when a user goal has a distinct trigger, input, and output.
- Add a reference when several skills need the same maintained knowledge.
- Add a script only for repeatable deterministic work.
- Add an MCP or app connection only when live data or external action is
  essential and the integration can be authorized safely.

Keep plugin version, `VERSION`, changelog, tests, and skill metadata aligned.
