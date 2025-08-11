import requests
from urllib.parse import urlparse

def run_test(url: str, username: str) -> tuple[bool, list[dict]]:
    print(f"Week4.py: Testing URL: {url} for user: {username}")
    checks = []

    # 1. Username Check
    username_passed = username in url
    checks.append({
        "name": "Contains username",
        "passed": username_passed,
        "message": f"URL must contain your username ({username})" if not username_passed else "OK"
    })

    # 2. Check that domain ends with '.web.app'
    try:
        parsed = urlparse(url)
        domain_valid = parsed.hostname.endswith('.web.app') if parsed.hostname else False
    except Exception as e:
        domain_valid = False

    checks.append({
        "name": "Domain ends with '.web.app'",
        "passed": domain_valid,
        "message": "URL must be hosted directly on .web.app (e.g., yourname.web.app)" if not domain_valid else "OK"
    })

    # 3. Reachability Check (status code 200)
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

    # Final result
    all_passed = all(c["passed"] for c in checks)

    print("== TEST RESULTS ==")
    for c in checks:
        print(f"{'[PASS]' if c['passed'] else '[FAIL]'} {c['name']}: {c['message']}")

    return all_passed, checks
