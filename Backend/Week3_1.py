import requests

def run_test(url: str, username: str) -> tuple[bool, list[dict]]:
    print(f"Week3_1.py: Testing URL: {url} for user: {username}")
    checks = []

    # 1. Username Check
    username_passed = username in url
    checks.append({
        "name": "Contains username",
        "passed": username_passed,
        "message": f"URL must contain your username ({username})" if not username_passed else "OK"
    })

    # 2. Contains pages.dev Check
    pages_dev_passed = "pages.dev" in url
    checks.append({
        "name": "Contains 'pages.dev'",
        "passed": pages_dev_passed,
        "message": "URL must contain 'pages.dev'" if not pages_dev_passed else "OK"
    })

    # 3. Reachability Check
    try:
        response = requests.get(url, timeout=5)
        status_passed = response.status_code == 200
        checks.append({
            "name": "URL reachable (status 200)",
            "passed": status_passed,
            "message": f"URL responded with status code {response.status_code}" if not status_passed else "OK"
        })

    except requests.RequestException as e:
        checks.append({
            "name": "URL reachable (status 200)",
            "passed": False,
            "message": f"Failed to reach URL: {str(e)}"
        })

    all_passed = all(c["passed"] for c in checks)
    print("== TEST RESULTS ==")
    for c in checks:
        print(f"{'[PASS]' if c['passed'] else '[FAIL]'} {c['name']}: {c['message']}")

    return all_passed, checks
