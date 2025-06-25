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

def run_test(url: str) -> tuple[bool, str]:
    print(f"Week1.py: Testing URL: {url}")

    if not url.startswith("https://"):
        message = "URL must start with https://"
        print(f"Week1.py: Test FAILED – {message}")
        return False, message

    if not any(provider in url for provider in ALLOWED_PROVIDERS):
        message = f"URL must contain a valid hosting provider ({', '.join(ALLOWED_PROVIDERS)})"
        print(f"Week1.py: Test FAILED – {message}")
        return False, message

    if "cloudservicesexample" not in url:
        message = "URL must contain 'cloudservicesexample'"
        print(f"Week1.py: Test FAILED – {message}")
        return False, message

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            message = "Test passed – URL is reachable and returned status code 200"
            print(f"Week1.py: {message}")
            return True, message
        else:
            message = f"URL responded with status code {response.status_code}"
            print(f"Week1.py: Test FAILED – {message}")
            return False, message
    except requests.RequestException as e:
        message = f"Request failed: {e}"
        print(f"Week1.py: Test FAILED – {message}")
        return False, message





