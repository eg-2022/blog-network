import subprocess

def update_packages():
    subprocess.run(
        ["sudo", "apt-get", "update"]
    )

def upgrade_packages():
    subprocess.run(
        ["sudo", "apt-get", "-y", "upgrade"]
    )

def check_packages():
    packages = ["nano", "vim", "mandoc"]

    subprocess.run(
        ["sudo", "apt-get", "install", "-y", "nano"],
        check=True
    )

def run():
    update_packages()
    upgrade_packages()
    check_packages()