#!/usr/bin/env python3
"""Unit tests for client module."""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict, List, Any
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Test GithubOrgClient.org returns correct value."""
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"payload": True})

    def test_public_repos_url(self) -> None:
        """Test GithubOrgClient._public_repos_url returns expected URL."""
        test_payload = {"repos_url": "http://example.com/repos"}
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test_org")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """Test GithubOrgClient.public_repos returns expected repo list."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        test_url = "http://example.com/repos"
        mock_get_json.return_value = test_payload
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_url
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            mock_get_json.assert_called_once_with(test_url)
            mock_public_repos_url.assert_called_once()
            self.assertEqual(result, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str,
                         expected: bool) -> None:
        """Test GithubOrgClient.has_license returns expected boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_name": "test_org",
        "org_payload": {"repos_url": "https://api.github.com/orgs/test_org/repos"},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}}
        ],
        "expected_repos": ["repo1", "repo2"],
        "apache2_repos": ["repo2"]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class by mocking requests.get with fixture payloads."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        def side_effect(url: str) -> Any:
            class MockResponse:
                def __init__(self, json_data: Dict):
                    self.json_data = json_data
                def json(self) -> Dict:
                    return self.json_data
            if url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            if url == f"https://api.github.com/orgs/{cls.org_name}":
                return MockResponse(cls.org_payload)
            return MockResponse({})
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class by stopping the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test GithubOrgClient.public_repos returns expected repos."""
        client = GithubOrgClient(self.org_name)
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test GithubOrgClient.public_repos with apache-2.0 license."""
        client = GithubOrgClient(self.org_name)
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
