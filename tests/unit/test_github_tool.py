"""Reproduction test for issue #50 — repo analysis output is missing `has_tests`.

Issue: https://github.com/ascherj/pathreview/issues/50

`GitHubTool._fetch_repo_metadata` already reports `has_readme`, but there is no
`has_tests` field describing whether a repository ships automated tests. This test
asserts that field exists in the repo-analysis output. It FAILS on the current code
(the field is absent) — that failure reproduces the gap. The Week 9 fix will make it
pass by adding a `has_tests` detector alongside `has_readme`.
"""

from unittest.mock import MagicMock, patch

import pytest

from agent.tools.github_tool import GitHubTool


@pytest.mark.unit
class TestGitHubToolHasTests:
    """Reproduction coverage for the missing `has_tests` field."""

    @staticmethod
    def _fake_repo_response():
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json = MagicMock(
            return_value={
                "name": "demo",
                "description": "A demo repo",
                "language": "Python",
                "stargazers_count": 3,
                "forks_count": 1,
                "open_issues_count": 0,
                "pushed_at": "2026-01-01T00:00:00Z",
                "topics": [],
                "homepage": "",
            }
        )
        return resp

    @patch("agent.tools.github_tool.httpx.head")
    @patch("agent.tools.github_tool.httpx.get")
    def test_repo_metadata_includes_has_tests(self, mock_get, mock_head):
        """Repo metadata should report whether the repo has tests (issue #50)."""
        mock_get.return_value = self._fake_repo_response()
        head_resp = MagicMock()
        head_resp.status_code = 200
        mock_head.return_value = head_resp

        tool = GitHubTool()
        result = tool.execute({"github_username": "octocat", "repo_name": "demo"})

        assert result.success is True
        # Mirrors the existing `has_readme` field; currently ABSENT -> reproduces #50.
        assert "has_tests" in result.data, (
            "Repo metadata is missing the `has_tests` field (issue #50)"
        )
        assert isinstance(result.data["has_tests"], bool)
