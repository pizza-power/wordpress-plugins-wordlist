import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

URL = "https://plugins.svn.wordpress.org/"
ROOT = Path(__file__).resolve().parents[1]

PLUGINS_FILE = ROOT / "plugins.txt"
README_FILE = ROOT / "README.md"

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    plugins = set()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.endswith("/") and href != "../":
            plugins.add(href.rstrip("/"))

    plugins = sorted(plugins)

    PLUGINS_FILE.write_text("\n".join(plugins) + "\n")

    updated = datetime.utcnow().strftime("%Y-%m-%d")

    README_FILE.write_text(
        f"""# WordPress Plugin Wordlist

A continuously updated wordlist of WordPress plugin slugs derived from the official WordPress SVN repository.

- Source: https://plugins.svn.wordpress.org/
- One plugin per line
- Intended for security testing and research

Last updated: {updated}
"""
    )

if __name__ == "__main__":
    main()