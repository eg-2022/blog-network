from pathlib import Path
import subprocess
import yaml

CURRENT_DIR = Path(__file__).parent
CONFIG_FILE = CURRENT_DIR / "packages.yaml"

def update_packages():
    print("[INFO] Updating packages...")
    subprocess.run(
        ["sudo", "apt-get", "update"]
    )

def upgrade_packages():
    print("[INFO] Upgrading packages")
    subprocess.run(
        ["sudo", "apt-get", "-y", "upgrade"]
    )

def load_packages():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    
    packages = []

    for category in config.get("packages", {}).values():
        packages.extend(category)

    return list(dict.fromkeys(packages))

def install_all_packages():

    print("[INFO] Installing packages: ")

    packages = load_packages()
    if not packages:
        print("No packages to install")
        return False
 
    subprocess.run(
        ["sudo", "apt-get", "install", "-y", *packages],
        check=True
    )

def run():
    update_packages()
    upgrade_packages()
    install_all_packages()

if __name__ == "__main__":
    run()