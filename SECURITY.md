# Security policy

## Supported release

Security fixes target the latest release on the default branch.

## Sensitive data

Never commit LinkedIn passwords, session cookies, access tokens, OAuth secrets,
private-message archives, unredacted exports, customer data, or the contents of
`.oyyo-linkedin/`.

The local utilities make no network calls and store no account credentials.
Manual mode works without an account connection. Automatic mode uses a browser
capability supplied by the user's AI workspace, and API mode uses an official
or otherwise authorized connector. Each adapter is a separate trust boundary.
Use the smallest useful access scope and explicit approval before every write.

Automatic mode must never ask for a password, session cookie, one-time code,
recovery code, or browser storage value in chat. The user signs in directly.
Stop on CAPTCHAs, account challenges, restriction notices, changed recipients,
or unexpected content.

API tokens belong in the host secret store or environment. The worker's doctor
command reports only whether expected environment variables are present and
never prints their values. The optional official API adapter sends a token only
to `https://api.linkedin.com` and requires `--confirm` for every write.

## Reporting

Report a vulnerability privately through the repository owner's GitHub profile
at https://github.com/vpicciuolo/. Do not include live credentials or another
person's private data in the report.

## Out of scope

Requests for stealth automation, scraping, account-limit evasion, fake
engagement, spam, or bypassing LinkedIn controls are not supported features.
