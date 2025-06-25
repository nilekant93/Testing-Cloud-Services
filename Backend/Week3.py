import requests

def run_test(url: str) -> tuple[bool, str]:
    print(f"Week3.py: Testing URL existence: {url}")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            message = "URL exists and returned status code 200"
            print(f"Week3.py: {message}")
            return True, message
        else:
            message = f"URL responded with status code {response.status_code}"
            print(f"Week3.py: Test FAILED – {message}")
            return False, message
    except requests.RequestException as e:
        message = f"Request failed: {e}"
        print(f"Week3.py: Test FAILED – {message}")
        return False, message
