#!/usr/bin/env bash
set -euo pipefail

# region Variables and helpers

# Colors
NO_FORMAT="\033[0m"
F_BOLD="\033[1m"
C_AQUA="\033[38;5;14m"
C_LIME="\033[38;5;10m"
C_GOLD1="\033[38;5;220m"

# Local variables
CURRENT_USER="$(id -un)"

# Prefixes
info() { printf "${C_AQUA}[INFO]${NO_FORMAT} %s\n" "$*"; }
ok() { printf "${C_LIME}[SUCCESS]${NO_FORMAT} %s\n" "$*"; }
title() { printf "${F_BOLD}${C_GOLD1}%s${NO_FORMAT}\n" "$*"; }
# endregion

# Check if the file exists, then automatically export all variables defined inside it
[ -f .env ] && set -o allexport && source .env && set +o allexport

# Create the group "maintainers" and add
# the current user to the maintainers group
title "STAGE 1: Setting up SSH server"

if getent group 'maintainers' > /dev/null 2>&1; then
    info "Group 'maintainers' exists already"
else
    info "Creating group 'maintainers'...";
    sudo groupadd maintainers;
    info "Adding user: '$CURRENT_USER' to group: 'maintainers'"
    sudo usermod -aG maintainers "$CURRENT_USER"
    ok "User: '$CURRENT_USER' was added to group: 'maintainers'"
fi

# Copy the files from sshd_config.d and clean original sshd_config.d directory
info "Removing old configurations files from /etc/ssh/ssh_config.d"
sudo rm -rf /etc/ssh/sshd_config.d/*
ok "Removed old configurations files from /etc/ssh/ssh_config.d"

info "Copying files to /etc/ssh/sshd_config.d/"
sudo cp -r ./sshd_config.d/* /etc/ssh/sshd_config.d/
ok "Copied files to /etc/ssh/sshd_config.d/"

# Including modular directives on /etc/ssh/sshd_config
info "Including modular directives on /etc/ssh/sshd_config"
echo "Include /etc/ssh/sshd_config.d/*.conf" | sudo tee /etc/ssh/sshd_config > /dev/null
ok "Included modular directives on /etc/ssh/sshd_config"

# Copy public keys from .env
info "Pulling public keys from: $GITHUB_SSH_KEY"
curl -fsSL "$GITHUB_SSH_KEY" -o "/home/$CURRENT_USER/.ssh/authorized_keys"
ok "Pulled public keys from: $GITHUB_SSH_KEY"

# Adding keys to 
info "Changing permissions to 600 in /home/$CURRENT_USER/.ssh/authorized_keys"
chmod 600 "/home/$CURRENT_USER/.ssh/authorized_keys"
ok "Changed permissions to 600 in /home/$CURRENT_USER/.ssh/authorized_keys"