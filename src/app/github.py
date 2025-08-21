import requests


class GitHub:
    def __init__(self, token, owner):
        self._token = token
        self._owner = owner
        self.base_url = "https://api.github.com"

    @property
    def token(self):
        return self._token

    @property
    def owner(self):
        return self._owner

    def get_repository(self, repo):
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

    def create_issue(self, repo, body):
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

    def get_issues(self, repo):
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

    def update_issue(self, repo, body, issue_number):
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

    def get_commits(self, repo):
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
