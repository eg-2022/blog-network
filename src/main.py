import os
import sys
import platform
from install import install_packages

def check_if_posix():
    if os.name != "posix":
        print(f"Not a valid operative system: {os.name}")
        return False

    return True

def check_if_debian_or_ubuntu():
    try:
        info = platform.freedesktop_os_release()
        os_id = info.get("ID", "").lower()
        os_like = info.get("ID_LIKE", "").lower()

        if os_id not in ("debian", "ubuntu") and "debian" not in os_like:
            print("This program requires Debian or Ubuntu.")
            return False   
    except OSError:
        print("Could not determine the operating system.")
        return False

    return True

def check_if_root():
    if os.getuid() != 0:
        print("Please, run this program as root.")
        return False

    return True

def main():
    checks = (
        check_if_posix,
        check_if_debian_or_ubuntu,
        check_if_root,
    )

    for check in checks:
        if not check():
            return 1

    install_packages.run()

    return 0

if __name__ == "__main__":
    sys.exit(main())