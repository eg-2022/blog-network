#!/usr/bin/env bash
set -euo pipefail

# Colors
NO_FORMAT="\033[0m"
F_BOLD="\033[1m"
C_AQUA="\033[38;5;14m"
C_LIME="\033[38;5;10m"

# Local variables
CURRENT_USER="$(id -un)"

# Check if the file exists, then automatically export all variables defined inside it
[ -f .env ] && set -o allexport && source .env && set +o allexport

# Create the group "maintainer" and add
# the current user to the maintainer group
echo -e "${F_BOLD}${C_AQUA}STAGE 1: SETTING UP SSH SERVER${NO_FORMAT}"

if getent group 'maintainers' > /dev/null 2>&1; then
    echo -e "${C_AQUA}[INFO]${NO_FORMAT} Group 'maintainers' exists already!"
else
    echo "Creating group 'maintainers'...";
    sudo groupadd maintainers;
    echo "Adding user: '$CURRENT_USER' to group: 'maintainers'"
    sudo usermod -aG maintainers "$CURRENT_USER"
    echo -e "${C_LIME}[SUCCESS]${NO_FORMAT} User: '$CURRENT_USER' was added to group: 'maintainers'"
fi

# Copy the files from sshd_config.d and clean original sshd_config.d directory
sudo rm -rf /etc/ssh/sshd_config.d/*
sudo cp -r ./sshd_config.d/* /etc/ssh/sshd_config.d/
echo "Include /etc/ssh/sshd_config.d/*.conf" | sudo tee /etc/ssh/sshd_config > /dev/null

# Copy public keys from .env
curl -fsSL "$GITHUB_SSH_KEY" -o "/home/$CURRENT_USER/.ssh/authorized_keys"
chmod 600 "/home/$CURRENT_USER/.ssh/authorized_keys"
