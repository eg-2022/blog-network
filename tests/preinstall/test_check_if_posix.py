from unittest.mock import patch

from preinstall import check_if_posix


def test_check_if_posix_returns_true():
    with patch("preinstall.check_if_posix.os.name", "posix"):
        assert check_if_posix() is True


def test_check_if_posix_returns_false():
    with patch("preinstall.check_if_posix.os.name", "nt"):
        assert check_if_posix() is False