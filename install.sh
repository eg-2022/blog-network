#!/usr/bin/env bash

set -e

echo "=== 1/6 --- Updating packages... ==="
sudo apt-get update

echo "=== 2/6 --- Installing curl... ==="
sudo apt-get install -y curl

echo "=== 3/6 --- Installing uv... ==="
curl -LsSf https://astral.sh/uv/install.sh | sh

# Export uv to the local environment
export PATH="$HOME/.local/bin:$PATH"

uv --version

echo "=== 4/6 --- Syncing dependencies ==="
uv sync

echo "=== 5/6 --- Executing installation ==="
uv run src/main.py

echo "=== 6/6 --- Removing uv ==="
uv_dir="$HOME/.local/bin/uv"
uvx_dir="$HOME/.local/bin/uvx"

rm -f "$uv_dir" "$uvx_dir"

echo "=== Done. Reboot your system. ==="
