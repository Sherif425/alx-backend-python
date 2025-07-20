#!/usr/bin/env python3
"""Unit tests for client module."""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict, List, Any
from client import GithubOrgClient
from utils import access_nested_map


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
            "https://api.github.com/orgs/{}".format(org_name))
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
        "org_name": "google",
        "org_payload": {"repos_url": "https://api.github.com/orgs/google/repos"},
        "repos_payload": [
            {
                "id": 7697149,
                "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                "name": "episodes.dart",
                "license": {
                    "key": "bsd-3-clause",
                    "name": "BSD 3-Clause \"New\" or \"Revised\" License",
                    "spdx_id": "BSD-3-Clause",
                    "url": "https://api.github.com/licenses/bsd-3-clause",
                    "node_id": "MDc6TGljZW5zZTU="
                }
            },
            {
                "id": 7776515,
                "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                "name": "cpp-netlib",
                "license": {
                    "key": "bsl-1.0",
                    "name": "Boost Software License 1.0",
                    "spdx_id": "BSL-1.0",
                    "url": "https://api.github.com/licenses/bsl-1.0",
                    "node_id": "MDc6TGljZW5zZTI4"
                }
            },
            {
                "id": 7968417,
                "node_id": "MDEwOlJlcG9zaXRvcnk3OTY4NDE3",
                "name": "dagger",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "id": 8165161,
                "node_id": "MDEwOlJlcG9zaXRvcnk4MTY1MTYx",
                "name": "ios-webkit-debug-proxy",
                "license": {
                    "key": "other",
                    "name": "Other",
                    "spdx_id": "NOASSERTION",
                    "url": None,
                    "node_id": "MDc6TGljZW5zZTA="
                }
            },
            {
                "id": 8459994,
                "node_id": "MDEwOlJlcG9zaXRvcnk4NDU5OTk0",
                "name": "google.github.io",
                "license": None
            },
            {
                "id": 8566972,
                "node_id": "MDEwOlJlcG9zaXRvcnk4NTY2OTcy",
                "name": "kratu",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "id": 8858648,
                "node_id": "MDEwOlJlcG9zaXRvcnk4ODU4NjQ4",
                "name": "build-debian-cloud",
                "license": {
                    "key": "other",
                    "name": "Other",
                    "spdx_id": "NOASSERTION",
                    "url": None,
                    "node_id": "MDc6TGljZW5zZTA="
                }
            },
            {
                "id": 9060347,
                "node_id": "MDEwOlJlcG9zaXRvcnk5MDYwMzQ3",
                "name": "traceur-compiler",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "id": 9065917,
                "node_id": "MDEwOlJlcG9zaXRvcnk5MDY1OTE3",
                "name": "firmata.py",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            }
        ],
        "expected_repos": [
            "episodes.dart",
            "cpp-netlib",
            "dagger",
            "ios-webkit-debug-proxy",
            "google.github.io",
            "kratu",
            "build-debian-cloud",
            "traceur-compiler",
            "firmata.py"
        ],
        "apache2_repos": ["dagger", "kratu", "traceur-compiler", "firmata.py"]
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
        self.mock_get.assert_any_call(
            f"https://api.github.com/orgs/{self.org_name}")
        self.mock_get.assert_any_call(self.org_payload["repos_url"])

    def test_public_repos_with_license(self) -> None:
        """Test GithubOrgClient.public_repos with apache-2.0 license."""
        with patch('utils.access_nested_map') as mock_access:
            def side_effect(nested_map: Dict, path: tuple) -> Any:
                try:
                    return access_nested_map(nested_map, path)
                except KeyError:
                    return None
            mock_access.side_effect = side_effect
            client = GithubOrgClient(self.org_name)
            result = client.public_repos(license="apache-2.0")
            self.assertEqual(result, self.apache2_repos)
            self.mock_get.assert_any_call(
                f"https://api.github.com/orgs/{self.org_name}")
            self.mock_get.assert_any_call(self.org_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
