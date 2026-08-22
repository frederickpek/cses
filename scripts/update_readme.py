import os
import re
import urllib.request
import urllib.parse
import http.cookiejar

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, ".env")
SVG_FILE = os.path.join(ROOT_DIR, "assets", "progress.svg")
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
    for chunk in html.split("<h2>")[1:]:
        name = chunk.split("</h2>")[0].strip()
        total = chunk.count('class="task"')
        if total == 0:
            continue
        solved = chunk.count("task-score icon full")
        categories[name] = (solved, total)
    return categories


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


def main():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    if not login(opener):
        print("Error: Login failed")
        exit(1)

    print("Fetching solve stats...")
    stats = get_stats(opener)

    for name, (solved, total) in stats.items():
        print(f"  {name}: {solved}/{total}")

    total_solved = sum(s for s, _ in stats.values())
    total_problems = sum(t for _, t in stats.values())
    print(f"\n  Total: {total_solved}/{total_problems}")

    update_svg(stats)
    print("\nassets/progress.svg updated.")


if __name__ == "__main__":
    main()
