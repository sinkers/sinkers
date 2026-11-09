"""Rewrite the block between the devlog markers in README.md from the devlog's articles.json."""
import json
import re
import sys
import urllib.request
from pathlib import Path

FEED = "https://sinkers.github.io/devlog/articles.json"
N = 5


def main() -> int:
    with urllib.request.urlopen(FEED, timeout=30) as r:
        items = json.load(r)
    items.sort(key=lambda a: a.get("date", ""), reverse=True)
    lines = [f"- [{a['title']}]({a['url']}) · {a['date']}" + (f" · {a['project']}" if a.get("project") else "")
             for a in items[:N]]
    readme = Path("README.md")
    text = readme.read_text()
    new = re.sub(r"(<!-- devlog:start -->\n).*?(<!-- devlog:end -->)",
                 lambda m: m.group(1) + "\n".join(lines) + "\n" + m.group(2), text, flags=re.S)
    if new != text:
        readme.write_text(new)
        print(f"updated with {len(lines)} articles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
