import requests
from urllib.parse import urlparse
import re

def run_test(site_url: str, readme_url: str, username: str) -> tuple[bool, list[dict]]:
    print(f"Week5.py: Testing site_url: {site_url} and readme_url: {readme_url} for user: {username}")
    checks = []

    # 1. Tarkistetaan että site_url sisältää käyttäjänimen
    site_url_valid_username = username in site_url
    checks.append({
        "name": "Site URL contains username",
        "passed": site_url_valid_username,
        "message": f"Site URL must contain your username ({username})" if not site_url_valid_username else "OK"
    })

    # 2. Repo-nimen poiminta site_url:sta
    try:
        parsed_site = urlparse(site_url)
        path_parts = parsed_site.path.strip('/').split('/')
        repo_name = path_parts[0] if path_parts else ''
        repo_found = bool(repo_name)
        checks.append({
            "name": "Repository name found in Site URL",
            "passed": repo_found,
            "message": f"Could not determine repository name from site URL" if not repo_found else "OK"
        })
    except Exception as e:
        repo_name = ''
        checks.append({
            "name": "Repository name extraction",
            "passed": False,
            "message": f"Error parsing repository name: {str(e)}"
        })

    # 3. Tarkistetaan että site_url sisältää github.io
    site_url_valid_domain = 'github.io' in site_url
    checks.append({
        "name": "Site URL contains 'github.io'",
        "passed": site_url_valid_domain,
        "message": "Site must be hosted on github.io domain" if not site_url_valid_domain else "OK"
    })

    # 4. Tarkistetaan että site_url on saavutettavissa
    try:
        response_site = requests.get(site_url, timeout=5)
        site_status_ok = response_site.status_code == 200
        checks.append({
            "name": "Site URL reachable (status 200)",
            "passed": site_status_ok,
            "message": f"Site URL responded with status {response_site.status_code}" if not site_status_ok else "OK"
        })
    except requests.RequestException as e:
        site_status_ok = False
        checks.append({
            "name": "Site URL reachable (status 200)",
            "passed": False,
            "message": f"Failed to reach site URL: {str(e)}"
        })

    # 5. Tarkistetaan että readme_url on saavutettavissa
    try:
        response_readme = requests.get(readme_url, timeout=5)
        readme_status_ok = response_readme.status_code == 200
        checks.append({
            "name": "README URL reachable (status 200)",
            "passed": readme_status_ok,
            "message": f"README URL responded with status {response_readme.status_code}" if not readme_status_ok else "OK"
        })
    except requests.RequestException as e:
        readme_status_ok = False
        checks.append({
            "name": "README URL reachable (status 200)",
            "passed": False,
            "message": f"Failed to reach README URL: {str(e)}"
        })

    # 6. Tarkistetaan että readme_url sisältää käyttäjänimen ja repo-nimen
    readme_url_valid_username = username in readme_url
    readme_url_valid_repo = repo_name in readme_url if repo_name else False

    checks.append({
        "name": "README URL contains username",
        "passed": readme_url_valid_username,
        "message": f"README URL must contain your username ({username})" if not readme_url_valid_username else "OK"
    })
    checks.append({
        "name": "README URL contains repository name",
        "passed": readme_url_valid_repo,
        "message": f"README URL must contain repository name ({repo_name})" if not readme_url_valid_repo else "OK"
    })

    # 7. Markdown-syntaksin tarkistus sisällöstä (valinnainen)
    if readme_status_ok:
        has_markdown_header = bool(re.search(r'^#', response_readme.text, re.MULTILINE))
        checks.append({
            "name": "README contains markdown headers (#)",
            "passed": has_markdown_header,
            "message": "README should contain at least one markdown header (#)" if not has_markdown_header else "OK"
        })
    else:
        checks.append({
            "name": "README markdown syntax check skipped",
            "passed": False,
            "message": "Could not check markdown syntax because README URL was unreachable"
        })

    # Lopullinen tulos
    all_passed = all(c["passed"] for c in checks)

    print("== WEEK5 TEST RESULTS ==")
    for c in checks:
        print(f"{'[PASS]' if c['passed'] else '[FAIL]'} {c['name']}: {c['message']}")

    return all_passed, checks
