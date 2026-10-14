#!/usr/bin/env bash
set -euo pipefail

# Create the group "maintainer" and add
# the current user to the maintainer group
{ sudo groupadd maintainer && sudo usermod -aG maintainer "$USER"; 
} 2>&1 | tee -a log.txt

# Copy the files from sshd_config.d and clean original sshd_config.d directory
rm -rf /etc/ssh/sshd_config.d/*
cp -r ./sshd_config.d/* /etc/ssh/sshd_config.d/*
echo "Include /etc/ssh/sshd_config.d/*.conf" > /etc/ssh/sshd_config
