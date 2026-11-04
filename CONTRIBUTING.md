# Contributing

Link a focused issue and describe the observable behavior being changed. Preserve
unrelated work and use a dedicated branch. Keep fixes, meaningful regressions and
affected documentation together.

For frontend work, use Node 22 or 24, install with `npm ci` in `frontend/`, then run:

```sh
npm run lint
npm run type-check
npm run build
npx playwright install chromium
npm test
npm audit --audit-level=high
```

Commit package-lock changes with dependency changes. Review new package
provenance, licenses and install scripts. Never commit `.env` values, model
artifacts, health data, logs, browser traces or generated build output.

Backend validation currently has setup and test-contract gaps; use
[issue #7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7)
and [the evidence record](docs/engineering-evidence.md) before claiming coverage.
Keep synthetic-model tests distinct from real-model inference and evaluation.

In a PR, state the issue, concrete before/after behavior, commands actually run,
remaining failures, compatibility effects and rollback. Agent review is not
independent human approval. Do not merge, release or deploy without authorization.

Do not put confidential security reports in public issues. Public vulnerability
reporting is currently disabled; maintainers can use draft repository security
advisories. No external private contact or response commitment is established by
this repository.
