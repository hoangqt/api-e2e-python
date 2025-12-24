import logging
import requests
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_random_exponential

logger = logging.getLogger(__name__)


class GitHub:
    def __init__(self, token: str, owner: str) -> None:
        self._token: str = token
        self._owner: str = owner
        self.base_url: str = "https://api.github.com"

    @property
    def token(self) -> str:
        return self._token

    @property
    def owner(self) -> str:
        return self._owner

    def get_repository(self, repo: str) -> Optional[requests.Response]:
        url = f"{self.base_url}/repos/{self.owner}/{repo}"
        logger.debug(f"Fetching repository from {url}")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException:
            return None

    def create_issue(
        self, repo: str, body: Dict[str, Any]
    ) -> Optional[requests.Response]:
        url = f"{self.base_url}/repos/{self.owner}/{repo}/issues"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            return response
        except requests.RequestException:
            return None

    def get_issues(
        self, repo: str, url: Optional[str] = None
    ) -> Optional[requests.Response]:
        if url is None:
            url = f"{self.base_url}/repos/{self.owner}/{repo}/issues"
            logger.debug(f"Fetching issues from {url}")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException:
            return None

    # Retry on failure with exponential backoff and jitter to avoid rate limiting,
    # transient network issues or potential collisions
    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(5))
    def update_issue(
        self, repo: str, body: Dict[str, Any], issue_number: int
    ) -> Optional[requests.Response]:
        url = f"{self.base_url}/repos/{self.owner}/{repo}/issues/{issue_number}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }

        try:
            response = requests.patch(url, headers=headers, json=body)
            response.raise_for_status()
            return response
        except requests.RequestException:
            return None

    def get_commits(self, repo: str) -> Optional[requests.Response]:
        url = f"{self.base_url}/repos/{self.owner}/{repo}/commits"
        logger.debug(f"Fetching commits from {url}")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }
        try:
            # Example of a timeout configuration workaround to missing request
            # cancellation feature
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response
        except requests.RequestException:
            return None
