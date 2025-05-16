# Week1.py

def run_test(url: str) -> bool:
    # Esimerkki: testaa että URL alkaa https:llä ja sisältää "fly.dev"
    print(f"Week1.py: Testing URL: {url}")
    if url.startswith("https://") and "fly.io" in url:
        print("Week1.py: Test PASSED")
        return True
    else:
        print("Week1.py: Test FAILED")
        return False


