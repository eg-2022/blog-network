import subprocess

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

def check_packages():
    packages = ["nano", "vim", "mandoc"]

    print("[INFO] Installing packages: ")
    subprocess.run(
        ["sudo", "apt-get", "install", "-y", "nano"],
        check=True
    )

def run():
    update_packages()
    upgrade_packages()
    check_packages()