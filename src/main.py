import sys
import preinstall
import install

def main():
    checks = (
        preinstall.posix.run,
        preinstall.debian_or_ubuntu.run,
        preinstall.root.run,

        install.setup_groups_and_users.run,
        install.install_packages.run,
        install.check_installed_packages.run,
        install.install_sshd_config_files.run,
    )

    for check in checks:
        if not check():
            return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())