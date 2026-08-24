import io
import os
import re
import sys
import shutil
import zipfile
import urllib.request
import urllib.parse
import http.cookiejar

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PY = os.path.join(ROOT_DIR, "scripts", "template.py")
TEMPLATE_CPP = os.path.join(ROOT_DIR, "scripts", "template.cpp")
ENV_FILE = os.path.join(ROOT_DIR, ".env")
BASE_URL = "https://cses.fi"
TASK_URL = f"{BASE_URL}/problemset/task/{{}}"
LOGIN_URL = f"{BASE_URL}/login"
TESTS_URL = f"{BASE_URL}/problemset/tests/{{}}/"


def build_opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def fetch(opener, url, data=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    if isinstance(data, bytes):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, headers=headers)
    with opener.open(req) as resp:
        return resp.read()


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


def login(opener):
    load_env()
    username = os.environ.get("CSES_USERNAME", "")
    password = os.environ.get("CSES_PASSWORD", "")
    if not username or not password:
        return False

    html = fetch(opener, LOGIN_URL).decode("utf-8")
    match = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
    if not match:
        print("Warning: Could not find CSRF token on login page")
        return False

    csrf_token = match.group(1)
    data = urllib.parse.urlencode({
        "csrf_token": csrf_token,
        "nick": username,
        "pass": password,
    }).encode("utf-8")

    resp_html = fetch(opener, LOGIN_URL, data=data).decode("utf-8")
    if "Log out" in resp_html or f">{username}<" in resp_html:
        return True

    print("Warning: Login may have failed (could not confirm session)")
    return False


CHAR_REPLACEMENTS = {
    "ü": "u",
    "-": "",
}


def to_snake_case(s):
    for old, new in CHAR_REPLACEMENTS.items():
        s = s.replace(old, new)
    s = re.sub(r"[^a-zA-Z0-9\s]", "", s)
    return "_".join(s.lower().split())


def parse_task_page(html):
    name_match = re.search(r"<h1>([^<]+)</h1>", html)
    category_match = re.search(r"<h4>([^<]+)</h4>", html)
    name = name_match.group(1).strip() if name_match else None
    category = category_match.group(1).strip() if category_match else None
    return name, category


def extract_csrf(html):
    match = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
    return match.group(1) if match else None


def download_tests(opener, task_id, tests_dir):
    try:
        tests_html = fetch(opener, TESTS_URL.format(task_id)).decode("utf-8")
    except urllib.error.HTTPError:
        return False

    csrf_token = extract_csrf(tests_html)
    if not csrf_token:
        return False

    data = urllib.parse.urlencode({
        "csrf_token": csrf_token,
        "download": "true",
    }).encode("utf-8")

    try:
        zip_bytes = fetch(opener, TESTS_URL.format(task_id), data=data)
    except urllib.error.HTTPError:
        return False

    if len(zip_bytes) < 100 or zip_bytes[:4] != b"PK\x03\x04":
        return False

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if name.endswith(".in") or name.endswith(".out"):
                content = zf.read(name)
                basename = os.path.basename(name)
                with open(os.path.join(tests_dir, basename), "wb") as f:
                    f.write(content)

    return True


def extract_examples(html):
    html_single = html.replace("\n", "\x00")
    examples = []

    pattern = r"<p>Input:</p>(?:\x00|\s)*<pre>(.*?)</pre>(?:\x00|\s)*<p>Output:</p>(?:\x00|\s)*<pre>(.*?)</pre>"
    for match in re.finditer(pattern, html_single):
        inp = match.group(1).replace("\x00", "\n").strip()
        out = match.group(2).replace("\x00", "\n").strip()
        examples.append((inp, out))

    return examples


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 load.py <task_id> [--cpp]")
        sys.exit(1)

    task_id = sys.argv[1]
    use_cpp = len(sys.argv) == 3 and sys.argv[2] == "--cpp"

    template = TEMPLATE_CPP if use_cpp else TEMPLATE_PY
    ext = ".cpp" if use_cpp else ".py"

    if not os.path.isfile(template):
        print(f"Error: template not found at {template}")
        sys.exit(1)

    opener = build_opener()

    logged_in = login(opener)

    print(f"Fetching problem info for task {task_id}...")
    task_html = fetch(opener, TASK_URL.format(task_id)).decode("utf-8")

    name, category = parse_task_page(task_html)
    if not name or not category:
        print(f"Error: Could not find task {task_id} on CSES problem set")
        sys.exit(1)

    print(f"Problem:  {name}")
    print(f"Category: {category}")

    category_slug = to_snake_case(category)
    problem_slug = f"{to_snake_case(name)}_{task_id}"

    category_dir = os.path.join(ROOT_DIR, "problems", category_slug)
    os.makedirs(category_dir, exist_ok=True)

    problem_file = os.path.join(category_dir, f"{problem_slug}{ext}")
    if os.path.isfile(problem_file):
        print(f"File already exists: {problem_file}")
    else:
        shutil.copy(template, problem_file)
        print(f"Created: {problem_file}")

    tests_dir = os.path.join(ROOT_DIR, "tests", task_id)
    if os.path.isdir(tests_dir):
        shutil.rmtree(tests_dir)
    os.makedirs(tests_dir)

    if logged_in:
        print("Logged in to CSES, downloading full test cases...")
        if download_tests(opener, task_id, tests_dir):
            count = len([f for f in os.listdir(tests_dir) if f.endswith(".in")])
            print(f"Downloaded {count} test case(s) to tests/{task_id}/")
        else:
            print("Could not download full tests.")
    else:
        print("No CSES credentials found.")
        print("Set CSES_USERNAME and CSES_PASSWORD in .env for full test cases.")

    examples = extract_examples(task_html)
    for i, (inp, out) in enumerate(examples, 1):
        with open(os.path.join(tests_dir, f"ex{i}.in"), "w") as f:
            f.write(inp + "\n")
        with open(os.path.join(tests_dir, f"ex{i}.out"), "w") as f:
            f.write(out + "\n")
    print(f"Extracted {len(examples)} example(s) to tests/{task_id}/")

    print("Done!")


if __name__ == "__main__":
    main()
