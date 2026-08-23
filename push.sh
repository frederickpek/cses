#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: ./push.sh <task_id>"
    echo "Example: ./push.sh 1094"
    exit 1
fi

TASK_ID="$1"

git pull --rebase

FILE=$(find problems/ -name "*_${TASK_ID}.py" 2>/dev/null | head -1)

if [ -z "$FILE" ]; then
    echo "Error: No solution file found for task $TASK_ID"
    exit 1
fi

BASENAME=$(basename "$FILE" .py)
NAME_PART="${BASENAME%_$TASK_ID}"
TITLE=$(echo "$NAME_PART" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g' | sed 's/ Ii\+$/\U&/')

git add "$FILE"
git commit -m "Solve $TITLE ($TASK_ID)"
git push
