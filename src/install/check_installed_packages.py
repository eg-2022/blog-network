import sys
import subprocess
from pathlib import Path
import yaml

CURRENT_DIR = Path(__file__).parent
CONFIG_FILE = CURRENT_DIR / "packages.yaml"

def load_packages():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    
    packages = []

    for category in config.get("packages", {}).values():
        packages.extend(category)

    return list(dict.fromkeys(packages))

def check_all_packages():
    print("[INFO] Checking packages: ")

    packages = load_packages()
    if not packages:
        print("No packages to check")
        return False

    missing_packages = []
 
    for package in packages:
        result = subprocess.run(
            ["dpkg", "-s", package],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            missing_packages.append(package)

    if missing_packages:
        for package in missing_packages:
            print(f"[ERROR] Package: {package} wasn't found.")
        return False

    print("[SUCCESS] Packages were installed successfully")
    return True

def run():
    if not check_all_packages():
        sys.exit(1)
    
if __name__ == "__main__":
    run()