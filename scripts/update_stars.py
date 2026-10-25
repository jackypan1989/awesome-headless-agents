#!/usr/bin/env python3
"""Refresh the ★ star counts on README entries hosted on GitHub or GitLab.

Usage: python3 scripts/update_stars.py [README.md]

Reads GITHUB_TOKEN from the environment if set (recommended: the anonymous
GitHub API allows only 60 requests per hour). Exits non-zero if any lookup
fails, leaving the file untouched.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request

ENTRY = re.compile(
    r"^(?P<head>- \[[^\]]+\]\((?P<url>[^)]+)\))"
    r"(?P<tags>(?: (?!★)[^\s-][^\s]*)*?)"
    r"(?: ★ [0-9.]+k?)?"
    r"(?P<rest> - .*)$"
)
GITHUB = re.compile(r"^https://github\.com/([^/]+/[^/#?]+)/?$")
GITLAB = re.compile(r"^https://gitlab\.com/([^#?]+?)/?$")


def fetch_json(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "awesome-headless-agents"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def stars_for(url, token):
    if m := GITHUB.match(url):
        return fetch_json(f"https://api.github.com/repos/{m.group(1)}", token)["stargazers_count"]
    if m := GITLAB.match(url):
        project = urllib.parse.quote(m.group(1), safe="")
        return fetch_json(f"https://gitlab.com/api/v4/projects/{project}")["star_count"]
    return None


def fmt(n):
    if n < 1000:
        return str(n)
    if n < 100_000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return f"{round(n / 1000)}k"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    token = os.environ.get("GITHUB_TOKEN")
    lines = open(path, encoding="utf-8").read().split("\n")
    failures = []

    for i, line in enumerate(lines):
        m = ENTRY.match(line)
        if not m or m.group("url").startswith("#"):
            continue
        try:
            n = stars_for(m.group("url"), token)
        except Exception as e:
            failures.append(f"{m.group('url')}: {e}")
            continue
        star = f" ★ {fmt(n)}" if n is not None else ""
        lines[i] = m.group("head") + m.group("tags") + star + m.group("rest")

    if failures:
        print("Star lookup failed:\n  " + "\n  ".join(failures), file=sys.stderr)
        sys.exit(1)
    open(path, "w", encoding="utf-8").write("\n".join(lines))


if __name__ == "__main__":
    main()
