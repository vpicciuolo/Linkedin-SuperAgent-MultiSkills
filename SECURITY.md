# Security policy

## Supported release

Security fixes target the latest release on the default branch.

## Sensitive data

Never commit LinkedIn passwords, session cookies, access tokens, OAuth secrets,
private-message archives, unredacted exports, customer data, or the contents of
`.oyyo-linkedin/`.

The base pack makes no network calls and does not access a LinkedIn account.
Treat any future connector, browser tool, or publishing integration as a
separate trust boundary. Use least-privilege permissions and an explicit user
approval before every external action.

## Reporting

Report a vulnerability privately through the repository owner's GitHub profile
at https://github.com/vpicciuolo/. Do not include live credentials or another
person's private data in the report.

## Out of scope

Requests for stealth automation, scraping, account-limit evasion, fake
engagement, spam, or bypassing LinkedIn controls are not supported features.
