# Project status and continuation

Last verified: 2026-11-04, Asia/Kolkata.
[Repository](https://github.com/aaron-seq/heart-diseases-prediction-tool) ·
[Project 13](https://github.com/users/aaron-seq/projects/13) ·
[scope/roadmap](PRODUCT.md) · [evidence](../engineering-evidence.md) ·
[milestone 1](https://github.com/aaron-seq/heart-diseases-prediction-tool/milestone/1).

## Current state

- Active goal: [#5](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/5),
  reproducible frontend build and configured health probe. Branch
  `codex/5-frontend-verification`; base `3583203`, frontend code `8007ce0`.
  Delivery/configuration documentation is committed after that code revision.
  [PR #24](https://github.com/aaron-seq/heart-diseases-prediction-tool/pull/24) is
  pushed and draft. Its [current-head checks](https://github.com/aaron-seq/heart-diseases-prediction-tool/pull/24/checks)
  and Project record hosted verification; no merge or deployment is inferred.
- Frontend implementation is locally verified: clean install, lint/types/build,
  six production-bundle Chromium regressions and fresh same-system review.
  Detailed commands, versions, Red/Green and limits are in the evidence record.
- No merge, release or deployment. Milestone/issues remain open pending review
  and required acceptance. Backend CI/runtime/model verification remains blocked;
  frontend success does not validate the whole repository.
- Follow-ups: [#23](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/23)
  reconciles moderate development-tool advisories; [#22](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/22)
  requires authoritative license/provenance evidence. No owner approval inferred.
- Confidential findings and patches have separate restricted records and a private
  remediation worktree. Consult those records with maintainer access; do not copy
  their details into public issues, commits or this checkpoint.

## Agents and validation

- Discovery: read-only architecture/security/correctness mapping; parent checked
  material source claims and reused existing issues.
- Baseline: install/test/scan attempts; parent verified final retained scan/source
  findings. Initial backend collection failed for missing TensorFlow; it was not
  a passing suite. Initial frontend install lacked a lockfile.
- Frontend implementer: isolated `codex/5-frontend-implementation`, source commit
  `0254508`, cherry-picked as `8007ce0`; tests/assertions/diff checked by parent.
- Restricted implementer: private patch with controlled-predictor HTTP evidence;
  parent/fresh verifier checked it separately. No public integration inferred.
- Fresh verifier: both scopes reviewed separately, tests and extra negative/boundary
  probes run. Its first attempt failed immediately on a usage limit, then resumed
  successfully without changing files. Agents are not independent human approval.
- Parent personally ran `npm ci --no-audit --no-fund`, lint, types, build, six browser
  tests and full/runtime npm audits. Local Windows/Node 22 passes; Node 24/Linux
  acceptance depends on actual current-head frontend CI. Audit: 15 moderate dev
  paths, zero high/critical; runtime-only zero detected. No suppression added.
- Bandit and direct Python audit remain triage inputs; limited history-token
  search found no candidates in its selected patterns. Unrun specialist scans,
  platform/model/container checks and security boundaries are listed in evidence.

## Resume here

1. Inspect `git status --short --branch`, `git log -3 --oneline`, `git worktree list`
   and the repository's open PRs/current-head checks. Verify visibility before
   operating on any restricted fork. Do not duplicate issues/Project/PRs.
2. Read #5 and the PR for latest exact-head CI/review state. Review the source and
   [test map](../engineering-evidence.md) before interpreting results.
3. For frontend changes, from `frontend/`: `npm ci`, `npm run lint`,
   `npm run type-check`, `npm run build`, `npx playwright install chromium`,
   `npm test`, `npm audit --audit-level=high`. No backend/training is needed.
4. Next whole-repository slice: resolve [#4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4)
   and [#12](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/12),
   then real-model acceptance under [#7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7)
   and container execution [#9](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/9).
   Verify held-out preprocessing in [#6](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/6)
   before restoring any accuracy claim.

Generated dependency/build/test directories stay ignored in the implementation
worktree. Raw logs/scanner reports and restricted drafts remain only in the
access-restricted session evidence folder outside this checkout; losing that
machine loses those raw artifacts. Versioned tests, GitHub records and the
restricted PR preserve the reproducible conclusions and continuation steps.
