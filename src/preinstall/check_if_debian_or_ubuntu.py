import platform
from helpers import status

def check_if_debian_or_ubuntu():
    try:
        info = platform.freedesktop_os_release()
        os_id = info.get("ID", "").lower()
        os_like = info.get("ID_LIKE", "").lower()

        if os_id not in ("debian", "ubuntu") and "debian" not in os_like:
            print(status.error("This program requires Debian or Ubuntu."))
            return False   
    except OSError:
        print(status.error("Could not determine the operating system."))
        return False

    return True

def run():
    return check_if_debian_or_ubuntu()