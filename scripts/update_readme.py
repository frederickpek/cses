import os
import re
import urllib.request
import urllib.parse
import http.cookiejar

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, ".env")
README_FILE = os.path.join(ROOT_DIR, "README.md")
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


def update_readme(stats):
    with open(README_FILE) as f:
        content = f.read()

    total_solved = sum(s for s, _ in stats.values())
    total_problems = sum(t for _, t in stats.values())

    lines = content.split("\n")
    new_lines = []
    in_table = False

    for line in lines:
        if line.startswith("| Problem Type"):
            in_table = True
            new_lines.append(line)
            continue
        if line.startswith("|---"):
            new_lines.append(line)
            continue

        if in_table and line.startswith("|"):
            if "**Total**" in line:
                new_lines.append(
                    f"| **Total**               |**{total_solved}/{total_problems}**      |"
                )
                in_table = False
                continue

            for name, (solved, total) in stats.items():
                if re.search(rf'\b{re.escape(name)}\b', line):
                    pad_name = f"{name:<24s}"
                    count_str = f"{solved}/{total}"
                    new_lines.append(f"| {pad_name}|{count_str:<15s}|")
                    break
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(README_FILE, "w") as f:
        f.write("\n".join(new_lines))


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

    update_readme(stats)
    print("\nREADME.md updated.")


if __name__ == "__main__":
    main()
