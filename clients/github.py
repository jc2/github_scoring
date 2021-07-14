import os
from json import JSONDecodeError

import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout

url_base = "https://api.github.com"
repo_api = url_base + "/repos/{}/{}"

headers = {
    "Authorization": os.getenv("GITHUB_TOKEN")
}


class GitHubClientError(Exception):

    NOT_ACCESSIIBLE_REPO = 0
    CONNECTION_ERROR = 1
    PARSING_ERROR = 2

    def __init__(self, code, message):
        self.code = code
        self.message = message


def test_connection():
    requests.get(url_base, timeout=0.5)


def fetch_repo_info(username, repo):

    url = repo_api.format(username, repo)
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
    except HTTPError as e:
        raise GitHubClientError(GitHubClientError.NOT_ACCESSIIBLE_REPO,
                                f"Can not get repo info. Repo does not exist or it is private: {str(e)}")
    except (ConnectTimeout, ReadTimeout) as e:
        raise GitHubClientError(GitHubClientError.CONNECTION_ERROR,
                                f"Can not connect to GitHub API: {str(e)}")

    try:
        return response.json()
    except JSONDecodeError as e:
        raise GitHubClientError(GitHubClientError.PARSING_ERROR,
                                f"There was a problem parsing data: {str(e)}")


def is_popular(username, repo):

    repo_info = fetch_repo_info(username, repo)

    try:
        score = int(repo_info.get("stargazers_count", "")) + 2 * int(repo_info.get("forks_count", ""))
    except ValueError as e:
        raise GitHubClientError(GitHubClientError.PARSING_ERROR,
                                f"Error parsing information from client: {str(e)}")

    return True if score >= 500 else False
