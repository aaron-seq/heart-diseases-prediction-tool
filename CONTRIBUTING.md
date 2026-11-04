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

For backend API work, use Python 3.11 or 3.13 in an isolated environment. From
`backend/`, run:

```sh
python -m pip install --require-hashes -r requirements-api-test.txt
python -m pip check
python -m pytest tests -q
python tests/smoke_api.py
```

The contract fixture injects a controlled predictor into the real service/app;
the smoke check runs real Uvicorn/HTTP without ML packages or artifacts. Keep
these results distinct from real-model inference/evaluation under
[#4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4) and
[#7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7).
Regenerate the hash locks from their `.in` files using the commands in
[the evidence record](docs/engineering-evidence.md#api-startup-milestone).

In a PR, state the issue, concrete before/after behavior, commands actually run,
remaining failures, compatibility effects and rollback. Agent review is not
independent human approval. Do not merge, release or deploy without authorization.

Do not put confidential security reports in public issues. Public vulnerability
reporting is currently disabled; maintainers can use draft repository security
advisories. No external private contact or response commitment is established by
this repository.
