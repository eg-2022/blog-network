import yaml
import unittest
from unittest.mock import patch

from install.install_packages import (
    load_packages,
    install_all_packages,
)


class TestLoadPackages(unittest.TestCase):

    @patch("install.install_packages.yaml.safe_load")
    @patch("install.install_packages.CONFIG_FILE")
    def test_load_packages_success(self, mock_config, mock_yaml):
        mock_yaml.return_value = {
            "packages": {
                "development": ["git", "python3"],
                "utilities": ["curl", "wget"]
            }
        }

        result = load_packages()

        self.assertEqual(
            result,
            ["git", "python3", "curl", "wget"]
        )

    @patch("install.install_packages.yaml.safe_load")
    @patch("install.install_packages.CONFIG_FILE")
    def test_load_packages_removes_duplicates(self, mock_config, mock_yaml):
        mock_yaml.return_value = {
            "packages": {
                "development": ["git", "python3"],
                "utilities": ["git", "curl"]
            }
        }

        result = load_packages()

        self.assertEqual(result, ["git", "python3", "curl"])

    @patch("install.install_packages.CONFIG_FILE")
    @patch("yaml.safe_load", return_value={})
    def test_load_packages_empty_config(self, mock_yaml, mock_config):
        mock_config.open.return_value.__enter__.return_value = None

        result = load_packages()

        self.assertEqual(result, [])

    @patch("install.install_packages.CONFIG_FILE")
    @patch("yaml.safe_load", side_effect=Exception("Invalid YAML"))
    def test_load_packages_invalid_config(self, mock_yaml, mock_config):
        with self.assertRaises(Exception):
            load_packages()


class TestInstallAllPackages(unittest.TestCase):

    @patch("install.install_packages.subprocess.run")
    @patch("install.install_packages.load_packages")
    def test_install_all_packages_success(self, mock_load, mock_run):
        mock_load.return_value = ["git", "curl", "wget"]

        result = install_all_packages()

        self.assertTrue(result)

        mock_run.assert_called_once_with(
            ["sudo", "apt-get", "install", "-y", "git", "curl", "wget"],
            check=True
        )

    @patch("install.install_packages.load_packages")
    def test_install_all_packages_empty(self, mock_load):
        mock_load.return_value = []

        result = install_all_packages()

        self.assertFalse(result)

    @patch("install.install_packages.load_packages")
    def test_install_all_packages_yaml_error(self, mock_load):
        mock_load.side_effect = yaml.parser.ParserError(
            "Invalid YAML syntax"
        )

        result = install_all_packages()

        self.assertFalse(result)

    @patch("install.install_packages.subprocess.run")
    @patch("install.install_packages.load_packages")
    def test_install_all_packages_subprocess_called(self, mock_load, mock_run):
        mock_load.return_value = ["git"]

        install_all_packages()

        mock_run.assert_called_once_with(
            ["sudo", "apt-get", "install", "-y", "git"],
            check=True
        )


if __name__ == "__main__":
    unittest.main()

