import os
import re
import sys
import time
import uuid
import urllib.request
import urllib.parse
import http.cookiejar

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, ".env")
BASE_URL = "https://cses.fi"
LOGIN_URL = f"{BASE_URL}/login"
SUBMIT_URL = f"{BASE_URL}/problemset/submit/{{}}/"
SEND_URL = f"{BASE_URL}/course/send.php"
STATUS_URL = f"{BASE_URL}/ajax/get_status.php?entry={{}}"
RESULT_URL = f"{BASE_URL}/problemset/result/{{}}/"

GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
NC = "\033[0m"

VALID_OPTIONS = {"pypy3", "cpython3", "--cpp"}


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


def build_opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def fetch(opener, url, data=None, content_type=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    if content_type:
        headers["Content-Type"] = content_type
    elif isinstance(data, bytes):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, headers=headers)
    resp = opener.open(req)
    return resp.read().decode("utf-8"), resp.geturl()


def login(opener):
    load_env()
    username = os.environ.get("CSES_USERNAME", "")
    password = os.environ.get("CSES_PASSWORD", "")
    if not username or not password:
        print("Error: CSES_USERNAME and CSES_PASSWORD required in .env")
        return False

    html, _ = fetch(opener, LOGIN_URL)
    match = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
    if not match:
        return False

    data = urllib.parse.urlencode({
        "csrf_token": match.group(1),
        "nick": username,
        "pass": password,
    }).encode("utf-8")

    resp, _ = fetch(opener, LOGIN_URL, data)
    return "Log out" in resp


def find_solution(task_id, cpp=False):
    ext = ".cpp" if cpp else ".py"
    problems_dir = os.path.join(ROOT_DIR, "problems")
    for root, _, files in os.walk(problems_dir):
        for f in files:
            if f.endswith(f"_{task_id}{ext}"):
                return os.path.join(root, f)
    return None


def submit(opener, task_id, solution_path, option):
    html, _ = fetch(opener, SUBMIT_URL.format(task_id))
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
    if not csrf:
        print("Error: Could not find CSRF token on submit page")
        return None

    with open(solution_path, "rb") as f:
        file_content = f.read()

    filename = os.path.basename(solution_path)
    boundary = uuid.uuid4().hex
    parts = []

    def add_field(name, value):
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}'.encode()
        )

    def add_file(name, fname, content):
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{fname}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n".encode() + content
        )

    add_field("csrf_token", csrf.group(1))
    add_field("task", task_id)
    add_field("lang", "C++" if option.startswith("C++") else "Python3")
    add_field("option", option)
    add_field("type", "course")
    add_field("target", "problemset")
    add_file("file", filename, file_content)

    body = b"\r\n".join(parts) + f"\r\n--{boundary}--\r\n".encode()
    content_type = f"multipart/form-data; boundary={boundary}"

    _, result_url = fetch(opener, SEND_URL, body, content_type)

    match = re.search(r"/result/(\d+)/", result_url)
    if not match:
        print("Error: Could not find submission ID")
        return None

    return match.group(1)


def poll_result(opener, entry_id):
    delay = 0.5
    for _ in range(60):
        status, _ = fetch(opener, STATUS_URL.format(entry_id))
        if "READY" in status or "COMPILE ERROR" in status:
            return True
        sys.stdout.write(f"\r{YELLOW}TESTING...{NC}")
        sys.stdout.flush()
        time.sleep(delay)
        delay = min(delay * 1.1, 2.0)
    return False


def show_result(opener, entry_id):
    html, _ = fetch(opener, RESULT_URL.format(entry_id))

    result_match = re.search(r'class="inline-score verdict (\w+)">([^<]+)<', html)
    if result_match:
        verdict_class = result_match.group(1)
        verdict_text = result_match.group(2)
        color = GREEN if verdict_class == "ac" else RED
        sys.stdout.write(f"\r{color}{verdict_text}{NC}                    \n")
    else:
        compile_err = re.search(r"COMPILE ERROR", html)
        if compile_err:
            sys.stdout.write(f"\r{RED}COMPILE ERROR{NC}              \n")
        else:
            sys.stdout.write(f"\rUNKNOWN RESULT              \n")

    print()
    tests = re.findall(
        r'<td >(#\d+)</td><td class="verdict (\w+)">([^<]+)</td><td >([^<]*)</td>',
        html,
    )

    if tests:
        max_test_len = max(len(t[0]) for t in tests)
        for test_num, verdict_class, verdict_text, time_s in tests:
            color = GREEN if verdict_class == "ac" else RED
            printf_time = time_s.strip() if time_s.strip() else ""
            print(f"  {color}{verdict_text:<12s}{NC}  {test_num:<{max_test_len}s}  {printf_time}")

    print()
    print(RESULT_URL.format(entry_id))


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 submit.py <task_id> [cpython3|pypy3]")
        print("Default: pypy3")
        sys.exit(1)

    task_id = sys.argv[1]
    option = sys.argv[2].lower() if len(sys.argv) == 3 else "pypy3"

    if option not in VALID_OPTIONS:
        print(f"Error: Invalid option '{option}'. Use 'cpython3', 'pypy3', or '--cpp'")
        sys.exit(1)

    use_cpp = option == "--cpp"

    solution_path = find_solution(task_id, cpp=use_cpp)
    if not solution_path:
        print(f"Error: No solution file found for task {task_id}")
        sys.exit(1)

    rel_path = os.path.relpath(solution_path, ROOT_DIR)
    if use_cpp:
        lang_display = "C++"
        option_display = "C++20"
    else:
        lang_display = f"Python3 ({'PyPy3' if option == 'pypy3' else 'CPython3'})"
        option_display = "PyPy3" if option == "pypy3" else "CPython3"

    print(f"Solution: {rel_path}")
    print(f"Language: {lang_display}")
    print()

    opener = build_opener()

    if not login(opener):
        print("Error: Login failed")
        sys.exit(1)

    print("Submitting...")
    entry_id = submit(opener, task_id, solution_path, option_display)
    if not entry_id:
        sys.exit(1)

    if not poll_result(opener, entry_id):
        print("\nError: Timed out waiting for results")
        sys.exit(1)

    show_result(opener, entry_id)


if __name__ == "__main__":
    main()
