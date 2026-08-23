import json
import os
import re
import urllib.request
import urllib.parse
import http.cookiejar
from collections import defaultdict
from datetime import datetime, timedelta, timezone

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, ".env")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SVG_FILE = os.path.join(ASSETS_DIR, "progress.svg")
TIMELINE_FILE = os.path.join(ASSETS_DIR, "timeline.svg")
CHECKLIST_FILE = os.path.join(ASSETS_DIR, "checklist.json")
PROBLEMS_DIR = os.path.join(ROOT_DIR, "problems")
BASE_URL = "https://cses.fi"
LOGIN_URL = f"{BASE_URL}/login"
PROBLEMSET_URL = f"{BASE_URL}/problemset/"


def load_env():
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, _, value = line.partition("=")
                if key and _ == "=":
                    os.environ.setdefault(key.strip(), value.strip())


def fetch(opener, url, data=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    if isinstance(data, bytes):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, headers=headers)
    with opener.open(req) as resp:
        return resp.read().decode("utf-8")


def login(opener):
    load_env()
    username = os.environ.get("CSES_USERNAME", "")
    password = os.environ.get("CSES_PASSWORD", "")
    if not username or not password:
        print("Error: CSES_USERNAME and CSES_PASSWORD required")
        return False

    html = fetch(opener, LOGIN_URL)
    match = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
    if not match:
        return False

    data = urllib.parse.urlencode({
        "csrf_token": match.group(1),
        "nick": username,
        "pass": password,
    }).encode("utf-8")

    resp = fetch(opener, LOGIN_URL, data)
    return "Log out" in resp


def get_stats(opener):
    html = fetch(opener, PROBLEMSET_URL)
    categories = {}
    solved_tasks = []
    for chunk in html.split("<h2>")[1:]:
        name = chunk.split("</h2>")[0].strip()
        total = chunk.count('class="task"')
        if total == 0:
            continue
        solved = chunk.count("task-score icon full")
        categories[name] = (solved, total)
        for m in re.finditer(
            r'<a href="/problemset/task/(\d+)">([^<]+)</a>.*?'
            r'class="task-score icon (full|)"',
            chunk, re.DOTALL,
        ):
            task_id, task_name, status = m.group(1), m.group(2), m.group(3)
            if status == "full":
                solved_tasks.append((int(task_id), task_name))
    return categories, solved_tasks


def update_svg(stats):
    total_solved = sum(s for s, _ in stats.values())
    total_problems = sum(t for _, t in stats.values())

    header_height = 35
    row_height = 30
    num_rows = len(stats)
    svg_height = header_height + num_rows * row_height + 40

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="580" height="{svg_height}">')
    lines.append('  <style>')
    lines.append('    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; fill: #24292f; }')
    lines.append('    text.header { font-size: 12px; font-weight: 600; fill: #656d76; }')
    lines.append('    text.count { text-anchor: end; font-size: 12px; fill: #656d76; }')
    lines.append('    line { stroke: #d0d7de; }')
    lines.append('    @media (prefers-color-scheme: dark) {')
    lines.append('      text { fill: #e6edf3; }')
    lines.append('      text.header { fill: #8b949e; }')
    lines.append('      text.count { fill: #8b949e; }')
    lines.append('      line { stroke: #30363d; }')
    lines.append('    }')
    lines.append('  </style>')
    lines.append('')
    lines.append('  <!-- Headers -->')
    lines.append('  <text class="header" x="10" y="16">Problem Type</text>')
    lines.append('  <text class="header" x="210" y="16">Progress</text>')
    lines.append('  <text class="header count" x="570" y="16">Solved</text>')
    lines.append('  <line x1="10" y1="26" x2="570" y2="26" stroke-width="1"/>')

    bar_width = 300
    for i, (name, (solved, total)) in enumerate(stats.items()):
        y_base = header_height + i * row_height
        text_y = y_base + 12
        rect_y = y_base
        fill_w = int(bar_width * solved / total) if total > 0 else 0

        lines.append('')
        lines.append(f'  <!-- {name}: {solved}/{total} -->')
        lines.append(f'  <text x="10" y="{text_y}">{name}</text>')
        lines.append(f'  <rect x="210" y="{rect_y}" width="{bar_width}" height="16" rx="4" fill="#e0e0e0"/>')
        lines.append(f'  <rect x="210" y="{rect_y}" width="{fill_w}" height="16" rx="4" fill="#4CAF50"/>')
        lines.append(f'  <text class="count" x="570" y="{text_y}">{solved} / {total}</text>')

    divider_y = header_height + num_rows * row_height
    total_text_y = divider_y + 22
    total_rect_y = divider_y + 10
    total_fill_w = int(bar_width * total_solved / total_problems) if total_problems > 0 else 0

    lines.append('')
    lines.append(f'  <!-- Total: {total_solved}/{total_problems} -->')
    lines.append(f'  <line x1="10" y1="{divider_y}" x2="570" y2="{divider_y}" stroke-width="1"/>')
    lines.append(f'  <text x="10" y="{total_text_y}" font-weight="bold">Total</text>')
    lines.append(f'  <rect x="210" y="{total_rect_y}" width="{bar_width}" height="16" rx="4" fill="#e0e0e0"/>')
    lines.append(f'  <rect x="210" y="{total_rect_y}" width="{total_fill_w}" height="16" rx="4" fill="#4CAF50"/>')
    lines.append(f'  <text class="count" x="570" y="{total_text_y}" font-weight="bold">{total_solved} / {total_problems}</text>')
    lines.append('</svg>')

    os.makedirs(os.path.dirname(SVG_FILE), exist_ok=True)
    with open(SVG_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


def load_checklist():
    if os.path.isfile(CHECKLIST_FILE):
        with open(CHECKLIST_FILE) as f:
            return json.load(f)
    return []


def save_checklist(checklist):
    os.makedirs(os.path.dirname(CHECKLIST_FILE), exist_ok=True)
    with open(CHECKLIST_FILE, "w") as f:
        json.dump(checklist, f, indent=2)
        f.write("\n")


def task_in_repo(task_id):
    for dirpath, _, filenames in os.walk(PROBLEMS_DIR):
        for fn in filenames:
            if fn.endswith(f"_{task_id}.py"):
                return True
    return False


def sync_checklist(solved_tasks):
    checklist = load_checklist()
    existing_ids = {entry["task_id"] for entry in checklist}
    added = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for task_id, task_name in solved_tasks:
        if task_id in existing_ids:
            continue
        if not task_in_repo(task_id):
            continue
        checklist.append({
            "task_id": task_id,
            "task_name": task_name,
            "date_solved": now,
        })
        added.append(task_name)
    checklist.sort(key=lambda e: e["date_solved"])
    save_checklist(checklist)
    return added


def update_timeline(checklist):
    if not checklist:
        return

    sgt = timezone(timedelta(hours=8))
    daily_counts = defaultdict(int)
    for entry in checklist:
        utc_dt = datetime.strptime(entry["date_solved"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        day = utc_dt.astimezone(sgt).strftime("%Y-%m-%d")
        daily_counts[day] += 1

    days = sorted(daily_counts.keys())
    cumulative = []
    running = 0
    for day in days:
        running += daily_counts[day]
        cumulative.append((day, running))

    padding_left = 70
    padding_right = 30
    padding_top = 40
    padding_bottom = 50
    chart_width = 500
    chart_height = 200
    svg_width = padding_left + chart_width + padding_right
    svg_height = padding_top + chart_height + padding_bottom

    raw_max = cumulative[-1][1]
    if raw_max <= 5:
        y_max = 5
    elif raw_max <= 10:
        y_max = 10
    else:
        y_max = ((raw_max + 9) // 10) * 10
    num_days = len(cumulative)

    def x_pos(i):
        if num_days == 1:
            return padding_left + chart_width / 2
        return padding_left + i * chart_width / (num_days - 1)

    def y_pos(count):
        if y_max == 0:
            return padding_top + chart_height
        return padding_top + chart_height - (count / y_max) * chart_height

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">')
    lines.append('  <style>')
    lines.append('    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #656d76; }')
    lines.append('    text.title { font-size: 13px; font-weight: 600; fill: #24292f; }')
    lines.append('    line.grid { stroke: #e8e8e8; stroke-width: 1; }')
    lines.append('    line.axis { stroke: #d0d7de; stroke-width: 1; }')
    lines.append('    @media (prefers-color-scheme: dark) {')
    lines.append('      text { fill: #8b949e; }')
    lines.append('      text.title { fill: #e6edf3; }')
    lines.append('      line.grid { stroke: #21262d; }')
    lines.append('      line.axis { stroke: #30363d; }')
    lines.append('    }')
    lines.append('  </style>')

    lines.append(f'  <text class="title" x="{padding_left}" y="20">Problems Solved Over Time</text>')

    y_ticks = 5
    for i in range(y_ticks + 1):
        val = int(y_max * i / y_ticks)
        y = y_pos(val)
        lines.append(f'  <line class="grid" x1="{padding_left}" y1="{y}" x2="{padding_left + chart_width}" y2="{y}"/>')
        lines.append(f'  <text x="{padding_left - 8}" y="{y + 4}" text-anchor="end">{val}</text>')

    lines.append(f'  <line class="axis" x1="{padding_left}" y1="{padding_top}" x2="{padding_left}" y2="{padding_top + chart_height}"/>')
    lines.append(f'  <line class="axis" x1="{padding_left}" y1="{padding_top + chart_height}" x2="{padding_left + chart_width}" y2="{padding_top + chart_height}"/>')

    if num_days <= 10:
        label_indices = list(range(num_days))
    else:
        step = max(1, num_days // 6)
        label_indices = list(range(0, num_days, step))
        if num_days - 1 not in label_indices:
            label_indices.append(num_days - 1)

    for i in label_indices:
        x = x_pos(i)
        label = cumulative[i][0][5:]
        lines.append(f'  <text x="{x}" y="{padding_top + chart_height + 18}" text-anchor="middle">{label}</text>')

    area_points = [f"{x_pos(0)},{padding_top + chart_height}"]
    for i, (_, count) in enumerate(cumulative):
        area_points.append(f"{x_pos(i)},{y_pos(count)}")
    area_points.append(f"{x_pos(num_days - 1)},{padding_top + chart_height}")
    lines.append(f'  <polygon points="{" ".join(area_points)}" fill="#4CAF50" opacity="0.15"/>')

    path_points = []
    for i, (_, count) in enumerate(cumulative):
        prefix = "M" if i == 0 else "L"
        path_points.append(f"{prefix}{x_pos(i)},{y_pos(count)}")
    lines.append(f'  <path d="{" ".join(path_points)}" fill="none" stroke="#4CAF50" stroke-width="2"/>')

    for i, (_, count) in enumerate(cumulative):
        lines.append(f'  <circle cx="{x_pos(i)}" cy="{y_pos(count)}" r="3" fill="#4CAF50"/>')

    lines.append('</svg>')

    with open(TIMELINE_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    if not login(opener):
        print("Error: Login failed")
        exit(1)

    print("Fetching solve stats...")
    stats, solved_tasks = get_stats(opener)

    for name, (solved, total) in stats.items():
        print(f"  {name}: {solved}/{total}")

    total_solved = sum(s for s, _ in stats.values())
    total_problems = sum(t for _, t in stats.values())
    print(f"\n  Total: {total_solved}/{total_problems}")

    update_svg(stats)
    print("\nassets/progress.svg updated.")

    added = sync_checklist(solved_tasks)
    if added:
        print(f"\nChecklist: added {len(added)} task(s): {', '.join(added)}")
    else:
        print("\nChecklist: up to date.")

    checklist = load_checklist()
    update_timeline(checklist)
    print("assets/timeline.svg updated.")


if __name__ == "__main__":
    main()
