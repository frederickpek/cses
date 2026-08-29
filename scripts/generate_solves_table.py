import json
import os
import re
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKLIST_FILE = os.path.join(ROOT_DIR, "assets", "checklist.json")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
OUTPUT_FILE = os.path.join(DOCS_DIR, "solves.md")
PROBLEMSET_URL = "https://cses.fi/problemset/list/"


def fetch_problemset():
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(PROBLEMSET_URL, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def parse_problems(html):
    problems = []
    for chunk in html.split("<h2>")[1:]:
        category = chunk.split("</h2>")[0].strip()
        for m in re.finditer(
            r'<a\s+href="/problemset/task/(\d+)"[^>]*>([^<]+)</a>'
            r'<span class="detail">(\d+)\s*/\s*\d+</span>',
            chunk,
        ):
            task_id = int(m.group(1))
            name = m.group(2).strip()
            solves = int(m.group(3))
            problems.append({
                "task_id": task_id,
                "name": name,
                "category": category,
                "solves": solves,
            })
    return problems


def load_solved_ids():
    if not os.path.isfile(CHECKLIST_FILE):
        return set()
    with open(CHECKLIST_FILE) as f:
        checklist = json.load(f)
    return {entry["task_id"] for entry in checklist}


def generate_markdown(problems, solved_ids):
    sgt = timezone(timedelta(hours=8))
    now = datetime.now(sgt).strftime("%-d %b %Y, %I:%M:%S %p (SGT)")
    lines = [
        "# CSES Problem Set — Solve Counts",
        "",
        f"Total problems: {len(problems)} | Solved: {len(solved_ids)}",
        "",
        f"Last updated: {now}",
        "",
        "Sorted by number of solves (descending).",
        "",
        "| # | Problem | Category | Solves | Solved |",
        "|--:|---------|----------|-------:|:------:|",
    ]
    problems.sort(key=lambda p: p["solves"], reverse=True)
    for i, p in enumerate(problems, 1):
        solved = "YES" if p["task_id"] in solved_ids else ""
        solves_fmt = f"{p['solves']:,}"
        link = f"[{p['name']}](https://cses.fi/problemset/task/{p['task_id']})"
        lines.append(f"| {i} | {link} | {p['category']} | {solves_fmt} | {solved} |")
    lines.append("")
    return "\n".join(lines)


def main():
    print("Fetching CSES problem set...")
    html = fetch_problemset()

    problems = parse_problems(html)
    print(f"Found {len(problems)} problems.")

    solved_ids = load_solved_ids()
    print(f"Checklist has {len(solved_ids)} solved problems.")

    md = generate_markdown(problems, solved_ids)

    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(md)
    print(f"Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
