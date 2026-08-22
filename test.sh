#!/usr/bin/env bash
set -euo pipefail

TIME_LIMIT=1
MEM_LIMIT_KB=$((512 * 1024))

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

if [ $# -ne 1 ]; then
    echo "Usage: ./test.sh <task_id>"
    echo "Example: ./test.sh 1068"
    exit 1
fi

TASK_ID="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TESTS_DIR="$SCRIPT_DIR/tests/$TASK_ID"

if [ ! -d "$TESTS_DIR" ]; then
    echo "Error: No tests found at tests/$TASK_ID/"
    exit 1
fi

PROBLEM_FILE=$(find "$SCRIPT_DIR/problems" -name "*_${TASK_ID}.py" 2>/dev/null | head -1)

if [ -z "$PROBLEM_FILE" ]; then
    echo "Error: No solution file found for task $TASK_ID"
    exit 1
fi

# Collect test names in order: examples first, then numbered
TESTS=()
for f in $(ls "$TESTS_DIR"/ex*.in 2>/dev/null | sort -V); do
    TESTS+=("$(basename "$f" .in)")
done
for f in $(ls "$TESTS_DIR"/[0-9]*.in 2>/dev/null | sort -V); do
    TESTS+=("$(basename "$f" .in)")
done

TOTAL=${#TESTS[@]}

# Find longest test name for alignment
MAX_NAME_LEN=0
for t in "${TESTS[@]}"; do
    [ ${#t} -gt $MAX_NAME_LEN ] && MAX_NAME_LEN=${#t}
done

echo "Solution: ${PROBLEM_FILE#$SCRIPT_DIR/}"
echo ""

PASS=0
FAIL=0

report_summary() {
    local omitted=$((TOTAL - PASS - FAIL))
    echo ""
    printf "${GREEN}%d passed${NC}, ${RED}%d failed${NC}, %d omitted\n" "$PASS" "$FAIL" "$omitted"
}

run_test() {
    local test_name="$1"
    local in_file="$TESTS_DIR/${test_name}.in"
    local out_file="$TESTS_DIR/${test_name}.out"

    if [ ! -f "$in_file" ] || [ ! -f "$out_file" ]; then
        return
    fi

    local tmp_out tmp_time tmp_err
    tmp_out=$(mktemp)
    tmp_time=$(mktemp)
    tmp_err=$(mktemp)
    trap "rm -f '$tmp_out' '$tmp_time' '$tmp_err'" RETURN

    local exit_code=0
    timeout "${TIME_LIMIT}s" /usr/bin/time -v -o "$tmp_time" \
        python3 "$PROBLEM_FILE" < "$in_file" > "$tmp_out" 2> "$tmp_err" \
        || exit_code=$?

    local peak_kb
    peak_kb=$(grep "Maximum resident set size" "$tmp_time" | grep -oP '\d+$') || peak_kb=0
    local mem_mb=$((peak_kb / 1024))

    if [ "$exit_code" -eq 124 ]; then
        FAIL=$((FAIL + 1))
        printf "${RED}TLE${NC}   %-${MAX_NAME_LEN}s  (>${TIME_LIMIT}s)\n" "$test_name"
        report_summary
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        exit 1
    fi

    if [ "$peak_kb" -gt "$MEM_LIMIT_KB" ]; then
        FAIL=$((FAIL + 1))
        printf "${RED}MLE${NC}   %-${MAX_NAME_LEN}s  (${used_mb}MB > $((MEM_LIMIT_KB / 1024))MB)\n" "$test_name"
        report_summary
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        exit 1
    fi

    if [ "$exit_code" -ne 0 ]; then
        FAIL=$((FAIL + 1))
        printf "${RED}RTE${NC}   %-${MAX_NAME_LEN}s  (exit code $exit_code)\n" "$test_name"
        echo ""
        cat "$tmp_err"
        report_summary
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        exit 1
    fi

    expected=$(sed 's/[[:space:]]*$//' "$out_file")
    actual=$(sed 's/[[:space:]]*$//' "$tmp_out")

    local time_raw time_s
    time_raw=$(grep "wall clock" "$tmp_time" | grep -oP '\d+:\d+\.\d+' | head -1) || time_raw="0:00.00"
    time_s=$(echo "$time_raw" | awk -F'[:]' '{printf "%.2fs", $1*60+$2}')

    if [ "$actual" = "$expected" ]; then
        PASS=$((PASS + 1))
        printf "${GREEN}PASS${NC}  %-${MAX_NAME_LEN}s  %6s  %4dMB\n" "$test_name" "$time_s" "$mem_mb"
    else
        FAIL=$((FAIL + 1))
        printf "${RED}WA${NC}    %-${MAX_NAME_LEN}s\n" "$test_name"
        echo ""
        echo "Input:"
        head -20 "$in_file"
        local lines
        lines=$(wc -l < "$in_file")
        if [ "$lines" -gt 20 ]; then
            echo "... ($lines lines total)"
        fi
        echo ""
        echo "Expected:"
        echo "$expected" | head -20
        lines=$(echo "$expected" | wc -l)
        if [ "$lines" -gt 20 ]; then
            echo "... ($lines lines total)"
        fi
        echo ""
        echo "Got:"
        echo "$actual" | head -20
        lines=$(echo "$actual" | wc -l)
        if [ "$lines" -gt 20 ]; then
            echo "... ($lines lines total)"
        fi
        report_summary
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        exit 1
    fi

    rm -f "$tmp_out" "$tmp_time" "$tmp_err"
}

for test_name in "${TESTS[@]}"; do
    run_test "$test_name"
done

echo ""
printf "${GREEN}All $PASS tests passed${NC}\n"
