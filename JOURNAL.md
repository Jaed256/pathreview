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
**Setup confirmation:** [ ] App runs locally at localhost:5173
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
