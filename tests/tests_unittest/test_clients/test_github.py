import json
from unittest.mock import patch

import pytest
import requests
from requests.exceptions import ConnectTimeout

from clients.github import fetch_repo_info, GitHubClientError, is_popular


@patch('clients.github.requests.get')
def test_github_fetch_ok(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 200
    mock_resp._content = json.dumps({"x": "y"}).encode()
    mock_get.return_value = mock_resp

    response = fetch_repo_info("django", "django")
    assert response == {"x": "y"}


@patch('clients.github.requests.get')
def test_github_fetch_not_found(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 404
    mock_resp._content = json.dumps({"x": "y"}).encode()
    mock_get.return_value = mock_resp

    with pytest.raises(GitHubClientError) as e:
        fetch_repo_info("django", "django")

    assert e.value.code == 0


@patch('clients.github.requests.get')
def test_github_fetch_private(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 401
    mock_resp._content = json.dumps({"x": "y"}).encode()
    mock_get.return_value = mock_resp

    with pytest.raises(GitHubClientError) as e:
        fetch_repo_info("django", "django")

    assert e.value.code == 0


@patch('clients.github.requests.get')
def test_github_fetch_parsing_1(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 200
    mock_resp._content = "hello".encode()
    mock_get.return_value = mock_resp

    with pytest.raises(GitHubClientError) as e:
        fetch_repo_info("django", "django")

    assert e.value.code == 2


@patch('clients.github.requests')
def test_github_fetch_timeout(mock_get):
    def get(*args, **kwargs):
        raise ConnectTimeout()

    mock_get.get.side_effect = get

    with pytest.raises(GitHubClientError) as e:
        fetch_repo_info("django", "django")

    assert e.value.code == 1


@patch('clients.github.requests.get')
@pytest.mark.parametrize(
    "stars,forks,expected_popular",
    [
        (0, 0, False),
        (199, 150, False),
        (200, 150, True),
        (500, 0, True),
        (0, 250, True),
        (500, 500, True),
    ]
)
def test_github_polular_ok_1(mock_get, stars, forks, expected_popular):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 200
    mock_resp._content = json.dumps({"stargazers_count": stars, "forks_count": forks}).encode()
    mock_get.return_value = mock_resp

    response = is_popular("django", "django")
    assert response == expected_popular
