import pytest
import time

from src.app.configuration import Configuration
from src.app.github import GitHub


class TestGitHubAPI:
    issueNumber = None

    @pytest.fixture(autouse=True)
    def github_setup(self):
        config = Configuration()
        self.github = GitHub(config.token, config.owner)
        self.repo = "sandbox"

        yield

        TestGitHubAPI._mark_issues_as_not_planned(self.github, self.repo)

    def test_get_repository(self):
        r = self.github.get_repository(self.repo)
        assert r is not None, "Error fetching GitHub repository"
        assert r.status_code == 200

    @pytest.mark.order(1)
    def test_create_issue(self):
        body = {
            "title": "Found a bug",
            "body": "This is a test issue created by Python automation",
            "assignees": ["hoangqt"],
            "labels": ["bug"],
        }
        r = self.github.create_issue(self.repo, body)
        assert r is not None, "Error creating GitHub issue"
        assert r.status_code == 201

    @pytest.mark.order(2)
    def test_get_issues(self):
        r = self.github.get_issues(self.repo)
        assert r is not None, "Error fetching GitHub issues"
        assert r.status_code == 200
        issues_list = r.json()
        if issues_list:
            for issue in issues_list:
                # Get the issue number of the first issue with title containing "Found a bug"
                if "Found a bug" in issue.get("title", ""):
                    TestGitHubAPI.issueNumber = issue["number"]
                    break

        # If not found, poll until timeout
        timeout_ms = 15_000  # 15 seconds
        poll_interval_ms = 500  # 0.5 seconds
        deadline = time.time() * 1000 + timeout_ms

        found = False
        while time.time() * 1000 < deadline:
            r = self.github.get_issues(self.repo)
            if r.status_code == 200:
                issues_list = r.json()
                for issue in issues_list:
                    if "Found a bug" in issue.get("title", ""):
                        TestGitHubAPI.issueNumber = issue["number"]
                        found = True
                        break
            if found:
                break

            time.sleep(poll_interval_ms / 1000)

    @pytest.mark.order(3)
    def test_update_issue(self):
        body = {
            "title": "Found a bug",
            "body": "This is a test issue created by Python automation",
            "assignees": ["hoangqt"],
            "labels": ["bug", "invalid"],
        }
        r = self.github.update_issue(self.repo, body, TestGitHubAPI.issueNumber)
        assert r is not None, "Error updating GitHub issue"
        assert r.status_code == 200

    def test_get_commits(self):
        r = self.github.get_commits(self.repo)
        assert r is not None, "Error fetching GitHub commits"
        assert r.status_code == 200
        commits_list = r.json()
        assert len(commits_list) > 0, "Expected at least one commit"

    @staticmethod
    def _mark_issues_as_not_planned(github, repo):
        """
        Mark all issues in the repo as 'not_planned' and closed
        """
        r = github.get_issues(repo)
        while r is not None:
            issues_list = r.json()
            if issues_list:
                for issue in issues_list:
                    issue_number = issue["number"]
                    body = {
                        "state": "closed",
                        "state_reason": "not_planned",
                    }
                    r_update = github.update_issue(repo, body, issue_number)
                    assert (
                        r_update is not None
                    ), f"Error updating GitHub issue #{issue_number}"
                    assert r_update.status_code == 200
            if "next" in r.links:
                r = github.get_issues(repo, r.links["next"]["url"])
            else:
                r = None
