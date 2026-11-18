import grp
import subprocess

MAINTAINERS_GROUP = "maintainers"

def check_if_group_created():
    try:
        grp.getgrnam(MAINTAINERS_GROUP)
        print(f"[INFO] Groups: {MAINTAINERS_GROUP} already exists.")
        return True
    except KeyError:
        pass

def create_maintainers_group():
    if check_if_group_created():
        return True

    try:
        subprocess.run(
            ["groupadd", MAINTAINERS_GROUP],
            check=True,
            text=True,
            capture_output=True
        )
        print(f"[INFO] Group: {MAINTAINERS_GROUP} was defined.")
        return True

    except FileNotFoundError:
        print("[ERROR] The groupadd command was not found.")

    except PermissionError:
        print("[ERROR] Insufficient permissions to execute groupadd.")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not create group: {e.stderr.strip()}")

    except OSError as e:
        print(f"[ERROR] Operating system error: {e}")

    return False

def run():
    return create_maintainers_group()