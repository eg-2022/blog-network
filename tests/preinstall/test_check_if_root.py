from unittest.mock import patch

from preinstall import check_if_root


def test_check_if_root_returns_true_when_root():
    with patch("preinstall.check_if_root.os.getuid", return_value=0):
        assert check_if_root() is True


def test_check_if_root_returns_false_when_not_root():
    with patch("preinstall.check_if_root.os.getuid", return_value=1000):
        assert check_if_root() is False