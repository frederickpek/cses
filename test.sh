#!/usr/bin/env bash
set -euo pipefail

TIME_LIMIT=1
MEM_LIMIT_KB=$((512 * 1024))

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

OS="$(uname)"

# Detect timeout command: GNU timeout, gtimeout, or process-group fallback
if command -v timeout &>/dev/null; then
    timeout_cmd() { timeout "${TIME_LIMIT}s" "$@"; }
elif command -v gtimeout &>/dev/null; then
    timeout_cmd() { gtimeout "${TIME_LIMIT}s" "$@"; }
else
    # Kill a process and all its descendants
    kill_tree() {
        local pid=$1
        local children
        children=$(pgrep -P "$pid" 2>/dev/null) || true
        for child in $children; do
            kill_tree "$child"
        done
        kill "$pid" 2>/dev/null
    }

    timeout_cmd() {
        "$@" &
        local pid=$!
        (sleep "$TIME_LIMIT" && kill_tree "$pid") &
        local watchdog=$!
        wait "$pid" 2>/dev/null
        local rc=$?
        kill "$watchdog" 2>/dev/null
        wait "$watchdog" 2>/dev/null
        if [ "$rc" -eq 137 ] || [ "$rc" -eq 143 ]; then
            return 124
        fi
        return "$rc"
    }
    BASH_TIMEOUT=1
fi

# Detect GNU time vs macOS time
USE_GNU_TIME=0
if command -v gtime &>/dev/null; then
    GNU_TIME_CMD="gtime"
    USE_GNU_TIME=1
elif [ "$OS" != "Darwin" ] && /usr/bin/time -v true &>/dev/null; then
    GNU_TIME_CMD="/usr/bin/time"
    USE_GNU_TIME=1
fi

RUN_ALL=0
FILTER=""
USE_CPP=0

usage() {
    echo "Usage: ./test.sh <task_id> [options]"
    echo "Example: ./test.sh 1068"
    echo "         ./test.sh 1068 -a"
    echo "         ./test.sh 1068 -i ex1"
    echo "         ./test.sh 1068 --cpp"
    echo ""
    echo "Options:"
    echo "  -a, --all          Run all tests (no early exit, compact output)"
    echo "  -i, --input NAME   Run only the specified test (e.g. -i 1, -i ex1)"
    echo "  --cpp              Use the C++ solution instead of Python"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

TASK_ID="$1"
shift

while [ $# -gt 0 ]; do
    case "$1" in
        -a|--all)
            RUN_ALL=1
            shift
            ;;
        -i|--input)
            [ $# -lt 2 ] && { echo "Error: -i requires a test name"; exit 1; }
            FILTER="$2"
            shift 2
            ;;
        --cpp)
            USE_CPP=1
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TESTS_DIR="$SCRIPT_DIR/tests/$TASK_ID"

if [ ! -d "$TESTS_DIR" ]; then
    echo "Error: No tests found at tests/$TASK_ID/"
    exit 1
fi

if [ "$USE_CPP" -eq 1 ]; then
    PROBLEM_FILE=$(find "$SCRIPT_DIR/problems" -name "*_${TASK_ID}.cpp" 2>/dev/null | head -1)
else
    PROBLEM_FILE=$(find "$SCRIPT_DIR/problems" -name "*_${TASK_ID}.py" 2>/dev/null | head -1)
fi

if [ -z "$PROBLEM_FILE" ]; then
    echo "Error: No solution file found for task $TASK_ID"
    exit 1
fi

if [ "$USE_CPP" -eq 1 ]; then
    CPP_BIN=$(mktemp)
    CPP_FLAGS="-O2 -std=c++20"
    # macOS clang lacks bits/stdc++.h; add a shim include path
    BITS_DIR=$(mktemp -d)
    mkdir -p "$BITS_DIR/bits"
    cat > "$BITS_DIR/bits/stdc++.h" <<'HEADER'
#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <climits>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
HEADER
    g++ $CPP_FLAGS -I"$BITS_DIR" -o "$CPP_BIN" "$PROBLEM_FILE" || { rm -rf "$BITS_DIR"; echo "Error: Compilation failed"; exit 1; }
    rm -rf "$BITS_DIR"
    RUN_CMD="$CPP_BIN"
    trap "rm -f '$CPP_BIN'" EXIT
else
    RUN_CMD="python3 $PROBLEM_FILE"
fi

# Collect test names in order: examples first, then numbered
TESTS=()
for f in $(ls "$TESTS_DIR"/ex*.in 2>/dev/null | sort -V); do
    TESTS+=("$(basename "$f" .in)")
done
for f in $(ls "$TESTS_DIR"/[0-9]*.in 2>/dev/null | sort -V); do
    TESTS+=("$(basename "$f" .in)")
done

# Filter to a single test if -i was given
if [ -n "$FILTER" ]; then
    FOUND=0
    for t in "${TESTS[@]}"; do
        if [ "$t" = "$FILTER" ]; then
            FOUND=1
            break
        fi
    done
    if [ "$FOUND" -eq 0 ]; then
        echo "Error: Test '$FILTER' not found in tests/$TASK_ID/"
        exit 1
    fi
    TESTS=("$FILTER")
fi

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

    if [ "$USE_GNU_TIME" -eq 1 ]; then
        # GNU time: -o writes time output to file, stderr stays python's
        timeout_cmd $GNU_TIME_CMD -v -o "$tmp_time" \
            $RUN_CMD < "$in_file" > "$tmp_out" 2> "$tmp_err" \
            || exit_code=$?
    else
        # macOS: wrap python in sh -c so its stderr is captured separately,
        # then time's stderr (the stats) is captured by the outer redirect
        { timeout_cmd /usr/bin/time -l \
            sh -c "$RUN_CMD < \"$in_file\" > \"$tmp_out\" 2> \"$tmp_err\"" ; } \
            2> "$tmp_time" || exit_code=$?
    fi

    local peak_kb=0
    if [ "$USE_GNU_TIME" -eq 1 ]; then
        peak_kb=$(awk -F': ' '/Maximum resident set size/{print $2}' "$tmp_time" 2>/dev/null) || peak_kb=0
    else
        # macOS reports bytes
        local peak_bytes
        peak_bytes=$(awk '/maximum resident set size/{print $1}' "$tmp_time" 2>/dev/null) || peak_bytes=0
        peak_kb=$((peak_bytes / 1024))
    fi
    local mem_mb=$((peak_kb / 1024))

    if [ "$exit_code" -eq 124 ]; then
        FAIL=$((FAIL + 1))
        printf "${RED}TLE${NC}   %-${MAX_NAME_LEN}s  (>${TIME_LIMIT}s)\n" "$test_name"
        if [ "$RUN_ALL" -eq 0 ]; then
            report_summary
            rm -f "$tmp_out" "$tmp_time" "$tmp_err"
            exit 1
        fi
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        return
    fi

    if [ "$peak_kb" -gt "$MEM_LIMIT_KB" ]; then
        FAIL=$((FAIL + 1))
        printf "${RED}MLE${NC}   %-${MAX_NAME_LEN}s  (${mem_mb}MB > $((MEM_LIMIT_KB / 1024))MB)\n" "$test_name"
        if [ "$RUN_ALL" -eq 0 ]; then
            report_summary
            rm -f "$tmp_out" "$tmp_time" "$tmp_err"
            exit 1
        fi
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        return
    fi

    if [ "$exit_code" -ne 0 ]; then
        FAIL=$((FAIL + 1))
        printf "${RED}RTE${NC}   %-${MAX_NAME_LEN}s  (exit code $exit_code)\n" "$test_name"
        if [ "$RUN_ALL" -eq 0 ]; then
            echo ""
            cat "$tmp_err"
            report_summary
            rm -f "$tmp_out" "$tmp_time" "$tmp_err"
            exit 1
        fi
        rm -f "$tmp_out" "$tmp_time" "$tmp_err"
        return
    fi

    expected=$(sed 's/[[:space:]]*$//' "$out_file")
    actual=$(sed 's/[[:space:]]*$//' "$tmp_out")

    local time_s
    if [ "$USE_GNU_TIME" -eq 1 ]; then
        local time_raw
        time_raw=$(awk '/wall clock/{match($0,/[0-9]+:[0-9]+\.[0-9]+/); print substr($0,RSTART,RLENGTH)}' "$tmp_time") || time_raw="0:00.00"
        time_s=$(echo "$time_raw" | awk -F'[:]' '{printf "%.2fs", $1*60+$2}')
    else
        # macOS: first line is "0.05 real 0.01 user 0.00 sys"
        time_s=$(awk '/real/{printf "%.2fs", $1}' "$tmp_time" 2>/dev/null) || time_s="0.00s"
    fi

    if [ "$actual" = "$expected" ]; then
        PASS=$((PASS + 1))
        printf "${GREEN}PASS${NC}  %-${MAX_NAME_LEN}s  %6s  %4dMB\n" "$test_name" "$time_s" "$mem_mb"
    else
        FAIL=$((FAIL + 1))
        printf "${RED}WA${NC}    %-${MAX_NAME_LEN}s\n" "$test_name"
        if [ "$RUN_ALL" -eq 0 ]; then
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
    fi

    rm -f "$tmp_out" "$tmp_time" "$tmp_err"
}

for test_name in "${TESTS[@]}"; do
    run_test "$test_name"
done

echo ""
if [ "$FAIL" -eq 0 ]; then
    printf "${GREEN}All $PASS tests passed${NC}\n"
else
    report_summary
    exit 1
fi
