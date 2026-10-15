#!/usr/bin/env bash
set -euo pipefail

# Global variables
CURRENT_USER="$(id -un)"

# Check if the file exists, then automatically export all variables defined inside it
[ -f .env ] && set -o allexport && source .env && set +o allexport

# Create the group "maintainer" and add
# the current user to the maintainer group
if getent group 'maintainers' > /dev/null 2>&1; then
    echo "Group 'maintainers' exists already!"
else
    echo "Creating group 'maintainers'...";
    sudo groupadd maintainers;
    echo "Adding user: '$CURRENT_USER' to group: 'maintainers'"
    sudo usermod -aG maintainers "$CURRENT_USER"
    echo "[SUCCESS] User: '$CURRENT_USER' was added to group: 'maintainers'"
fi

# Copy the files from sshd_config.d and clean original sshd_config.d directory
sudo rm -rf /etc/ssh/sshd_config.d/*
sudo cp -r ./sshd_config.d/* /etc/ssh/sshd_config.d/
echo "Include /etc/ssh/sshd_config.d/*.conf" | sudo tee /etc/ssh/sshd_config > /dev/null

# Copy public keys from .env
curl -fsSL "$GITHUB_SSH_KEY" -o "/home/$CURRENT_USER/.ssh/authorized_keys"
chmod 600 "/home/$CURRENT_USER/.ssh/authorized_keys"
