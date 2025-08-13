import requests
from urllib.parse import urlparse

def run_test(url: str, username: str) -> tuple[bool, list[dict]]:
    print(f"Week2.py: Testing URL: {url} for user: {username}")
    checks = []

    # 1. Domain check: must contain "amplifyapp.com"
    try:
        parsed = urlparse(url)
        domain_valid = parsed.hostname and "amplifyapp.com" in parsed.hostname
    except Exception:
        domain_valid = False

    checks.append({
        "name": "Domain contains 'amplifyapp.com'",
        "passed": bool(domain_valid),
        "message": "OK" if domain_valid else "URL must be hosted on AWS Amplify (domain must contain 'amplifyapp.com')"
    })

    # 2. Reachability check (status code must be 200)
    try:
        response = requests.get(url, timeout=5)
        status_passed = response.status_code == 200
        checks.append({
            "name": "URL reachable (status 200)",
            "passed": status_passed,
            "message": "OK" if status_passed else f"URL responded with status code {response.status_code}"
        })
    except requests.RequestException as e:
        checks.append({
            "name": "URL reachable (status 200)",
            "passed": False,
            "message": f"Failed to reach URL: {str(e)}"
        })

    # Final result: both checks must pass
    all_passed = all(c["passed"] for c in checks)

    print("== TEST RESULTS ==")
    for c in checks:
        print(f"{'[PASS]' if c['passed'] else '[FAIL]'} {c['name']}: {c['message']}")

    return all_passed, checks
