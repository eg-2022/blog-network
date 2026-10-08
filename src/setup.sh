#!/usr/bin/env bash
set -euo pipefail

# Create the group "maintainer" and add
# the current user to the maintainer group
{ sudo groupadd maintainer && sudo usermod -aG maintainer "$USER"; 
} 2>&1 | tee -a log.txt