# Manual, automatic, and API modes

OYYO LinkedIn SuperAgent uses one skill set with three execution adapters. A
skill decides what should happen. The selected mode decides how the current
state is read and how an approved action reaches LinkedIn.

## Quick decision

Choose manual mode when safety, portability, or complete website coverage
matters more than speed. Choose automatic mode when the AI workspace has a
browser or computer-use tool and you accept LinkedIn's account-policy risk.
Choose API mode when you have an approved LinkedIn application and need stable,
structured actions supported by its scopes.

You can change modes without rebuilding voice, strategy, stories, or content
history. Those files stay in `.oyyo-linkedin/`.

## Capability matrix

Availability changes with the LinkedIn UI, account type, company-page role,
API product, and OAuth scope. This matrix describes the intended routing, not a
promise that LinkedIn exposes every control to every account.

| Workflow | Manual | Automatic | Official API |
| --- | --- | --- | --- |
| Audit visible profile | user supplies text or screenshots | inspect signed-in profile | limited identity/profile fields when approved |
| Analyze recent posts | URLs, screenshots, or export | inspect profile/activity and analytics UI | read access may require restricted permissions |
| Analyze actual posting times | export or saved log | collect visible timestamps | use returned timestamps when read scope exists |
| Draft content | yes | yes | yes |
| Publish a member post | user pastes and publishes | browser action after approval | supported with the relevant member social permission |
| Comment, reply, or react | user performs action | browser action after approval | available only through supported, granted social APIs |
| Edit profile sections | exact guided changes | browser action after approval | generally not the same surface as website profile editing |
| Manage a company page | guided changes | browser action for an authorized admin | requires organization products, scopes, and a qualifying page role |
| Inbox and connections | guided changes | browser action after approval | not assumed; depends on restricted partner products |
| Delete content | guided deletion | browser action after approval | only when the API and granted scope support the target |

## Access scopes

`read` permits live inspection in the selected mode. `publish` adds content and
engagement actions. `manage` adds profile, page, inbox, connections, and
deletion workflows where the adapter supports them. A scope only defines what
the worker may prepare. It does not pre-approve a public or destructive change.

## Automatic-mode risk

LinkedIn states that third-party software or browser extensions may not scrape,
modify, or automate activity on its website. A browser-capable AI worker can
technically operate visible controls, but that does not make the activity
permitted by LinkedIn. Account restrictions are possible.

Automatic mode therefore requires an explicit acknowledgement. It also stops
on CAPTCHAs, security challenges, restrictions, unexpected recipients, changed
content, or unclear account state. The project does not contain stealth or
evasion features.

## Credentials

The user signs in directly in automatic mode. In API mode, the token belongs in
the AI host's secret store or an environment variable such as
`LINKEDIN_ACCESS_TOKEN`. Never paste a password, cookie, one-time code, recovery
code, client secret, access token, or refresh token into a prompt, state file,
issue, or commit.

The worker config stores environment-variable names, not secret values. Its
doctor command says `set` or `missing` without printing the value.

## Approval and receipts

Read-only work can proceed after the user grants the session scope. Each live
write requires the final target and content to be shown immediately before the
action. Approval applies to one action. It does not roll forward to later posts,
messages, profile changes, connections, or deletions.

The queue makes this distinction visible:

```text
pending_approval -> approved -> succeeded
                               -> failed
pending_approval -> cancelled
ready (read-only) -> succeeded | failed
```

A receipt records what the worker attempted and the result. It never stores the
password, token, cookie, private browser state, or full private message body.

## Setup commands

```bash
python plugins/linkedin-superagent-multiskills/scripts/oyyo_linkedin.py init
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode set manual --scope manage
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py doctor
```

Automatic mode needs the acknowledgement flag only after the warning is read
and accepted:

```bash
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode set automatic --scope manage --acknowledge-risk
```

API mode checks for token, actor URN, and LinkedIn API version environment
variables without revealing their values:

```bash
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py mode set api --scope publish --api-scope openid --api-scope w_member_social
python plugins/linkedin-superagent-multiskills/scripts/oyyo_worker.py doctor
```

The bundled official adapter supports a narrow set of approved operations:

```bash
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py whoami
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py publish-text approved-post.txt --confirm
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py comment urn:li:activity:123 approved-comment.txt --confirm
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py like urn:li:activity:123 --confirm
python plugins/linkedin-superagent-multiskills/scripts/linkedin_api.py delete-post urn:li:share:123 --confirm
```

Each write must correspond to an approved worker action. A command can still
fail when the application lacks the required LinkedIn product, scope, page
role, API version, or ownership of the target resource.

Read the active skill's output before executing a queued action. The worker
utility manages state and approvals; the AI workspace supplies the browser or
official API adapter.

## Official references

- [LinkedIn automated activity policy](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin)
- [LinkedIn API access and OAuth products](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn Comments API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api)
