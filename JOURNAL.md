# Module 3 Journal — PathReview

A running record of my Module 3 contribution work on the [pathreview](https://github.com/ascherj/pathreview) project.

## Week 7 — Issue selection

**Issue Link:** https://github.com/ascherj/pathreview/issues/50
**Issue title:** Add a `has_tests` boolean to the repo analysis output
**Tier:** [x] Tier 1 [ ] Tier 2 [ ] Tier 3

**Problem summary:**
PathReview analyzes a candidate's GitHub repositories and produces a structured summary of
each repo, but that summary currently says nothing about whether the repo actually ships
automated tests. Because a visible test suite is a strong signal of engineering maturity on
a portfolio, this is a real gap in what the analysis reports. The task is to add a
`has_tests` boolean to the repo analysis output, computed by checking a repository for common
test markers — a `tests/` or `test/` directory, a `pytest.ini`, or files matching
`test_*.py`. The work lives in the agent's repo-analysis tools (`agent/tools/repo_analyzer.py`
and `agent/tools/github_tool.py`) and the schema that shapes their output. A successful fix
surfaces `has_tests` for every analyzed repo and is covered by a unit test, so downstream
scoring and feedback can factor test coverage into a portfolio review.

**Branch name:** feat/50-repo-analysis-has-tests
**Setup confirmation:** [x] App runs locally at localhost:5173
**Cohort ledger:** [x] Issue added to cohort ledger (Section 1c, row 103)

### "Is this right for me?" — selection notes
- **Scope is contained.** The issue names the exact files to touch and the exact markers to
  detect; estimated effort is 2–4 hours, which fits a first contribution to a large codebase.
- **No deep architecture knowledge required.** It's additive — a new boolean field plus its
  detection logic — rather than a change that ripples across the RAG/agent pipeline.
- **Clear acceptance criteria.** "Detect `tests/`/`test/`, `pytest.ini`, or `test_*.py` and
  surface a boolean" is easy to verify with a unit test, so I'll know when it's done.
- **Good first issue + Tier 1**, labeled `agent`, `enhancement`, `tests` — aligned with where
  I want to build confidence before taking on a harder Week 8/9 issue.

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/Jaed256/pathreview/commits/feat/50-repo-analysis-has-tests

**Reproduction summary:**
I added a unit test (`tests/unit/test_github_tool.py`) that mocks the GitHub API and asserts
the repo-analysis metadata built by `GitHubTool._fetch_repo_metadata` includes a `has_tests`
boolean. Running it fails on `assert "has_tests" in result.data` — the returned dict contains
`has_readme` but no `has_tests` — which reproduces the gap exactly where the fix will go.

**PLAN.md Link:** https://github.com/Jaed256/pathreview/blob/feat/50-repo-analysis-has-tests/PLAN.md

**Walkthrough video (recommended):** (not recorded)

**Blockers or open questions:**
- Which GitHub endpoint to use for file detection — a single recursive git-tree call vs the
  contents API — given rate limits and tree truncation on very large repos.
- Whether `has_tests` should be consumed downstream (review scoring/schema) or only surfaced
  in the tool output for the scope of this issue.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Implemented the `has_tests` detector in `agent/tools/github_tool.py`. Added a
`_has_tests(username, repo_name, default_branch)` helper — mirroring the existing
`_has_readme` — that reads the repository git tree once via the GitHub API and returns
`True` if it finds a `tests/` or `test/` directory, a `pytest.ini`, or any `test_*.py`
file, and wired the result into `_fetch_repo_metadata` next to `has_readme`. PLAN.md
sub-tasks 1, 2, and the error-handling part of 4 are done. Unit tests cover every marker
plus the no-marker and API-error cases — `pytest tests/unit/test_github_tool.py` → 7 passed.

**Next steps:**
Run the full `make check` / `make test-unit`, document any pre-existing failures, open the
PR to `ascherj/pathreview`, and get peer feedback before marking it ready for review.

**Blockers:**
`github_tool.py` already fails black/ruff formatting checks on `main` (unrelated to this
change) — confirming my additions introduce no *new* failures.

### Check-in 2 (end of week)

**PR Link:** https://github.com/ascherj/pathreview/pull/945
**Branch:** feat/50-repo-analysis-has-tests

**What you built:**
Added a `has_tests` boolean to the repo-analysis output. A new `_has_tests` helper on
`GitHubTool` fetches the repository's git tree once and detects a `tests/`/`test/`
directory, a `pytest.ini`, or any `test_*.py` file; the value is surfaced in
`_fetch_repo_metadata` alongside `has_readme`. On any API error it degrades to `False`
rather than raising, so a detection failure never breaks analysis.

**Tests added or updated:**
`tests/unit/test_github_tool.py` — the reproduction test now passes, plus new cases for a
`tests/` directory, a singular `test/` directory, `pytest.ini`, a `test_*.py` file, the
no-marker (→ False) case, and a tree-API-error (graceful → False) case.

**Self-review confirmation:** [x] make check passes (no new failures) [x] make test-unit passes
(In this codebase `github_tool.py` has pre-existing formatting/lint flags on `main`; this
change introduces no new failures — documented in the PR description.)

**Draft PR feedback received from:** none
