#!/usr/bin/env python3
"""
Generate PacktPublishing Index
================================
Fetches ALL repositories from the PacktPublishing GitHub organization
and generates a complete, alphabetically-organized PACKT_INDEX.md.

Usage:
    # With a GitHub token (recommended — higher rate limits)
    GITHUB_TOKEN=your_token python scripts/generate_packt_index.py

    # Without token (rate-limited to 60 requests/hour)
    python scripts/generate_packt_index.py

    # Custom output file
    python scripts/generate_packt_index.py --output MY_INDEX.md

    # Dry run (fetch only, no file write)
    python scripts/generate_packt_index.py --dry-run
"""

import argparse
import datetime
import json
import os
import sys
import time
import urllib.request
import urllib.error
from collections import defaultdict

ORG = "PacktPublishing"
API_BASE = "https://api.github.com"
PER_PAGE = 100
OUTPUT_FILE = "PACKT_INDEX.md"


def make_request(url: str, token: str) -> dict:
    """Make a GitHub API request with optional authentication."""
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "LibraryOfAlexandria-IndexBot/1.0")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            remaining = int(resp.headers.get("X-RateLimit-Remaining", 999))
            reset_time = int(resp.headers.get("X-RateLimit-Reset", 0))
            if remaining < 5:
                wait = max(0, reset_time - int(time.time())) + 5
                print(f"⏳ Rate limit almost reached. Waiting {wait}s...")
                time.sleep(wait)
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("❌ Rate limited. Set GITHUB_TOKEN for higher limits.")
            print("   Create token at: https://github.com/settings/tokens")
            sys.exit(1)
        raise


def fetch_all_repos(token: str) -> list:
    """Fetch all repositories from the PacktPublishing organization."""
    repos = []
    page = 1

    print(f"🔍 Fetching repos from {ORG}...")
    while True:
        url = f"{API_BASE}/orgs/{ORG}/repos?type=public&sort=full_name&per_page={PER_PAGE}&page={page}"
        data = make_request(url, token)

        if not data:
            break

        repos.extend(data)
        count = len(repos)
        print(f"   Page {page}: fetched {len(data)} repos (total so far: {count})", end="\r")

        if len(data) < PER_PAGE:
            break
        page += 1

    print(f"\n✅ Fetched {len(repos)} total repositories")
    return repos


def generate_markdown(repos: list) -> str:
    """Generate the complete PACKT_INDEX.md content."""
    # Group alphabetically
    groups = defaultdict(list)
    for r in sorted(repos, key=lambda x: x["name"].lower()):
        name = r["name"].lstrip("-").lstrip(" ")
        letter = name[0].upper() if name else "#"
        if not letter.isalpha():
            letter = "#"
        groups[letter].append(r)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []

    lines.append("# 📚 PacktPublishing Complete Repository Index")
    lines.append("")
    lines.append(f"> Auto-generated on **{now}**  ")
    lines.append(f"> **{len(repos):,}** public repositories indexed from [PacktPublishing](https://github.com/PacktPublishing)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🔍 Quick Navigation")
    lines.append("")

    all_letters = sorted(groups.keys())
    toc_items = [f"[{l}](#{l.lower()}-{len(groups[l])}-repos)" for l in all_letters]
    for i in range(0, len(toc_items), 13):
        lines.append(" · ".join(toc_items[i : i + 13]))
    lines.append("")
    lines.append("---")
    lines.append("")

    for letter in all_letters:
        repos_in_group = groups[letter]
        lines.append(f"## {letter} ({len(repos_in_group)} repos)")
        lines.append("")
        lines.append("| Repository | Description | Language | ⭐ |")
        lines.append("|------------|-------------|----------|----|")
        for r in repos_in_group:
            name = r["name"]
            url = r["html_url"]
            desc = (r.get("description") or "").replace("|", "\\|")
            if len(desc) > 90:
                desc = desc[:87] + "..."
            lang = r.get("language") or ""
            stars = r.get("stargazers_count", 0)
            stars_str = f"⭐ {stars}" if stars > 0 else ""
            lines.append(f"| [{name}]({url}) | {desc} | {lang} | {stars_str} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate PacktPublishing index")
    parser.add_argument("--output", default=OUTPUT_FILE, help="Output markdown file")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--dry-run", action="store_true", help="Fetch only, don't write file")
    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("⚠️  No GITHUB_TOKEN set. Using unauthenticated requests (60/hour limit).")
        print("   For full index generation, set GITHUB_TOKEN environment variable.")
        print()

    repos = fetch_all_repos(token)

    if args.dry_run:
        print(f"🏃 Dry run — not writing {args.output}")
        return

    content = generate_markdown(repos)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)

    size_kb = len(content) / 1024
    print(f"📄 Written to {args.output} ({size_kb:.1f} KB, {len(repos):,} repos)")


if __name__ == "__main__":
    main()
