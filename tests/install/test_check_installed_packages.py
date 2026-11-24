
import subprocess
import yaml

from install.check_installed_packages import (
    load_packages,
    check_all_packages,
)


def test_load_packages_success(monkeypatch, tmp_path):
    config_file = tmp_path / "packages.yaml"

    config_file.write_text(
        """
packages:
  system:
    - curl
    - git
  development:
    - python3
    - git
""",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "install.check_installed_packages.CONFIG_FILE",
        config_file
    )

    result = load_packages()

    assert result == ["curl", "git", "python3"]


def test_load_packages_empty_yaml(monkeypatch, tmp_path):
    config_file = tmp_path / "packages.yaml"
    config_file.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        "install.check_installed_packages.CONFIG_FILE",
        config_file
    )

    result = load_packages()

    assert result == []


def test_load_packages_without_packages_key(monkeypatch, tmp_path):
    config_file = tmp_path / "packages.yaml"
    config_file.write_text(
        "other_key: value",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "install.check_installed_packages.CONFIG_FILE",
        config_file
    )

    result = load_packages()

    assert result == []


def test_load_packages_invalid_yaml(monkeypatch, tmp_path):
    config_file = tmp_path / "packages.yaml"
    config_file.write_text(
        "packages: [unclosed",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "install.check_installed_packages.CONFIG_FILE",
        config_file
    )

    try:
        load_packages()
        assert False, "Expected YAML ParserError"
    except yaml.parser.ParserError:
        pass


def test_check_all_packages_success(monkeypatch, capsys):
    monkeypatch.setattr(
        "install.check_installed_packages.load_packages",
        lambda: ["curl", "git"]
    )

    monkeypatch.setattr(
        "install.check_installed_packages.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="Package installed",
            stderr=""
        )
    )

    result = check_all_packages()

    captured = capsys.readouterr()

    assert result is True
    assert "Packages were installed successfully" in captured.out


def test_check_all_packages_missing_package(monkeypatch, capsys):
    monkeypatch.setattr(
        "install.check_installed_packages.load_packages",
        lambda: ["curl", "git"]
    )

    def mock_run(command, **kwargs):
        if command[-1] == "git":
            return subprocess.CompletedProcess(
                args=command,
                returncode=1,
                stdout="",
                stderr="Package not found"
            )

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="Package installed",
            stderr=""
        )

    monkeypatch.setattr(
        "install.check_installed_packages.subprocess.run",
        mock_run
    )

    result = check_all_packages()

    captured = capsys.readouterr()

    assert result is False
    assert "Package: git wasn't found." in captured.out


def test_check_all_packages_multiple_missing(monkeypatch, capsys):
    monkeypatch.setattr(
        "install.check_installed_packages.load_packages",
        lambda: ["curl", "git"]
    )

    monkeypatch.setattr(
        "install.check_installed_packages.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0],
            returncode=1,
            stdout="",
            stderr="Package not found"
        )
    )

    result = check_all_packages()

    captured = capsys.readouterr()

    assert result is False
    assert "Package: curl wasn't found." in captured.out
    assert "Package: git wasn't found." in captured.out


def test_check_all_packages_empty(monkeypatch, capsys):
    monkeypatch.setattr(
        "install.check_installed_packages.load_packages",
        lambda: []
    )

    result = check_all_packages()

    captured = capsys.readouterr()

    assert result is False
    assert "No packages to check" in captured.out


def test_check_all_packages_yaml_parser_error(monkeypatch, capsys):
    def mock_load_packages():
        raise yaml.parser.ParserError("Invalid YAML")

    monkeypatch.setattr(
        "install.check_installed_packages.load_packages",
        mock_load_packages
    )

    result = check_all_packages()

    captured = capsys.readouterr()

    assert result is False
    assert "There's an error, on syntax:" in captured.out


def test_check_all_packages_calls_dpkg(monkeypatch):
    packages = ["curl", "git", "python3"]
    executed_commands = []

    monkeypatch.setattr(
        "install.check_installed_packages.load_packages",
        lambda: packages
    )

    def mock_run(command, **kwargs):
        executed_commands.append(command)

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="",
            stderr=""
        )

    monkeypatch.setattr(
        "install.check_installed_packages.subprocess.run",
        mock_run
    )

    result = check_all_packages()

    assert result is True
    assert executed_commands == [
        ["dpkg", "-s", "curl"],
        ["dpkg", "-s", "git"],
        ["dpkg", "-s", "python3"],
    ]

