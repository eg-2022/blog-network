import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).parent / "files" / "sshd_config.d"
DESTINATION = Path("/etc/ssh/sshd_config.d")

def check_source_directory(source: Path):
    # Check if /etc/ssh/sshd_config.d exists

    print(source)

    if not Path.exists(source):
        print("[ERROR] Source directory not found. Installation could have gone wrong.")
        sys.exit(1)    
        return False
    
    return True

def check_destination_directory(destination: Path):
    print(destination)
    # Check if /etc/ssh/ exists
    if not Path.exists(destination):
        print("[ERROR] Destination directory not found. Installation could have gone wrong.")
        sys.exit(1)
        return False

    return True

def copy_directory_to_source(source: str, destination: str):
    # Copy files from SOURCE to DESTINATION
    try:
        shutil.copytree(src=source,
                dst=destination,
                dirs_exist_ok=True)
    except FileExistsError as e:
        print(f"[ERROR] {e}")
        return False

    return True

def run():
    checks = (
        lambda: check_source_directory(SOURCE),
        lambda: check_destination_directory(DESTINATION),
    )

    for check in checks:
        if not check():
            return False

    if not copy_directory_to_source(SOURCE, DESTINATION):
        return False

    return True