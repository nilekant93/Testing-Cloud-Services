import requests

ALLOWED_PROVIDERS = [
    "fly.dev",
    "render",
    "digitalocean",
    "hetzner",
    "oracle",
    "upcloud",
    "azure"
]

def run_test(url: str, username: str) -> tuple[bool, list[dict]]:
    print(f"Week1.py: Testing URL: {url} for user: {username}")

    checks = []

    # 1. HTTPS Check
    https_passed = url.startswith("https://")
    checks.append({
        "name": "Starts with https://",
        "passed": https_passed,
        "message": "URL must start with https://" if not https_passed else "OK"
    })

    # 2. Provider Check
    provider_passed = any(provider in url for provider in ALLOWED_PROVIDERS)
    checks.append({
        "name": "Valid hosting provider",
        "passed": provider_passed,
        "message": (
            f"URL must contain a valid hosting provider ({', '.join(ALLOWED_PROVIDERS)})"
            if not provider_passed else "OK"
        )
    })

    # 3. Username Check
    username_passed = username in url
    checks.append({
        "name": "Contains username",
        "passed": username_passed,
        "message": f"URL must contain your username ({username})" if not username_passed else "OK"
    })

    # 4. Reachability Check (only if https passed)
    if https_passed:
        try:
            response = requests.get(url, timeout=5)
            reachable_passed = response.status_code == 200
            checks.append({
                "name": "URL reachable (status 200)",
                "passed": reachable_passed,
                "message": (
                    f"URL responded with status code {response.status_code}"
                    if not reachable_passed else "OK"
                )
            })
        except requests.RequestException:
            checks.append({
                "name": "URL reachable (status 200)",
                "passed": False,
                "message": "Failed to reach URL"
            })
    else:
        checks.append({
            "name": "URL reachable (status 200)",
            "passed": False,
            "message": "Not tested due to invalid URL format"
        })

    all_passed = all(c["passed"] for c in checks)
    print("== TEST RESULTS ==")
    for c in checks:
        print(f"{'[PASS]' if c['passed'] else '[FAIL]'} {c['name']}: {c['message']}")

    return all_passed, checks
