import requests
from typing import Optional, Dict, Any


class GitHub:
    def __init__(self, token, owner) -> None:
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

    def create_issue(self, repo: str, body: Dict[str, Any]) -> Optional[requests.Response]:
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

    def get_issues(self, repo: str) -> Optional[requests.Response]:
        url = f"{self.base_url}/repos/{self.owner}/{repo}/issues"
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

    def update_issue(self, repo: str, body: Dict[str, Any], issue_number: int) -> Optional[requests.Response]:
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
