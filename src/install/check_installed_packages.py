import sys
import subprocess
from pathlib import Path
import yaml
from helpers import status

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
    print(status.info("Checking packages..."))

    packages = []

    try:
        packages = load_packages()
    except yaml.parser.ParserError as e:
        print(status.error(f"There's an error, on syntax: {e}."))
        return False

    if not packages:
        print(status.error("No packages to check"))
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
            print(status.error(f"Package: {package} wasn't found."))
        return False

    print(status.success("Packages were installed successfully"))
    return True

def run():
   return check_all_packages()