#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: ./push.sh <task_id>"
    echo "Example: ./push.sh 1094"
    exit 1
fi

TASK_ID="$1"

git pull --rebase

PY_FILE=$(find problems/ -name "*_${TASK_ID}.py" 2>/dev/null | head -1)
CPP_FILE=$(find problems/ -name "*_${TASK_ID}.cpp" 2>/dev/null | head -1)

if [ -z "$PY_FILE" ] && [ -z "$CPP_FILE" ]; then
    echo "Error: No solution file found for task $TASK_ID"
    exit 1
fi

# Use whichever file we find to derive the title
REF_FILE="${PY_FILE:-$CPP_FILE}"
REF_EXT="${REF_FILE##*.}"
BASENAME=$(basename "$REF_FILE" ".$REF_EXT")
NAME_PART="${BASENAME%_$TASK_ID}"
TITLE=$(echo "$NAME_PART" | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); if($NF ~ /^Ii+$/) $NF=toupper($NF)}1')

[ -n "$PY_FILE" ] && git add "$PY_FILE"
[ -n "$CPP_FILE" ] && git add "$CPP_FILE"
git commit -m "Solve $TITLE ($TASK_ID)"
git push
