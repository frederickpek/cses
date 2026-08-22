#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: ./load.sh <task_id>"
    echo "Example: ./load.sh 1068"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/scripts/load.py" "$1"
