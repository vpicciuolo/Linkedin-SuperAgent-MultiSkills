# Contributing

Contributions are welcome under the MIT License.

## Before opening a pull request

1. Keep each skill focused on one recognizable user goal.
2. Put shared rules in references instead of copying them into every skill.
3. Preserve the draft-first approval gate and the untrusted-content boundary.
4. Do not add scraping, stealth automation, credential collection, fake
   engagement, bulk unsolicited outreach, or detector-evasion claims.
5. Add tests for deterministic scripts and meaningful edge cases.
6. Update `VERSION` and `CHANGELOG.md` when behavior changes.
7. Preserve third-party license notices.

Run:

```bash
python plugins/linkedin-superagent-multiskills/scripts/validate_pack.py
python -m unittest discover -s plugins/linkedin-superagent-multiskills/tests -v
```

Pull requests should explain the user problem, expected behavior, test evidence,
and any privacy or platform-policy impact.
