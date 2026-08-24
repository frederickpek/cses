#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: ./load.sh <task_id> [--cpp]"
    echo "Example: ./load.sh 1068"
    echo "         ./load.sh 1068 --cpp"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/scripts/load.py" "$@"
