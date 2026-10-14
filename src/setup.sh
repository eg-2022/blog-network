#!/usr/bin/env bash
set -euo pipefail

# Global variables
CURRENT_USER="$(echo $USER)"

# Check if the file exists, then automatically export all variables defined inside it
[ -f .env ] && set -o allexport && source .env && set +o allexport

# Create the group "maintainer" and add
# the current user to the maintainer group
{ sudo groupadd maintainer && sudo usermod -aG maintainers "$USER"; 
} 2>&1 | tee -a log.txt

# Copy the files from sshd_config.d and clean original sshd_config.d directory
sudo rm -rf /etc/ssh/sshd_config.d/*
sudo cp -r ./sshd_config.d/* /etc/ssh/sshd_config.d/
echo "Include /etc/ssh/sshd_config.d/*.conf" | sudo tee /etc/ssh/sshd_config > /dev/null

# Copy public keys from .env
curl -fsSL "$GITHUB_SSH_KEY" -o "/home/$CURRENT_USER/.ssh/authorized_keys"
chmod 644 "/home/$CURRENT_USER/.ssh/authorized_keys"
