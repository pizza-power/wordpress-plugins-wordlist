import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

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
            plugin_name = href.rstrip("/")
            # Decode URL-encoded plugin names (e.g., %d0%af... -> actual characters)
            try:
                decoded = unquote(plugin_name, encoding='utf-8')
                plugins.add(decoded)
            except Exception:
                # If decoding fails, use original
                plugins.add(plugin_name)

    plugins = sorted(plugins)
    plugin_count = len(plugins)

    PLUGINS_FILE.write_text("\n".join(plugins) + "\n")

    updated = datetime.utcnow().strftime("%Y-%m-%d")

    README_FILE.write_text(
        f"""# WordPress Plugin Wordlist

A continuously updated wordlist of WordPress plugin slugs derived from the official WordPress SVN repository.

- Source: https://plugins.svn.wordpress.org/
- One plugin per line
- Intended for security testing and research

**Total entries:** {plugin_count:,}

Last updated: {updated}
"""
    )

if __name__ == "__main__":
    main()
