#!/usr/bin/env python3
"""
Quick Upload Script for The Library of Alexandria
==================================================
Upload documents to the repository via the GitHub API.

Usage:
    python upload.py --file mybook.pdf --dest docs/PDFs
    python upload.py --file mybook.pdf --dest docs/PDFs --token YOUR_TOKEN --message "Add mybook.pdf"
    python upload.py --url https://example.com/file.pdf --dest docs/PDFs --filename mybook.pdf

Requirements:
    pip install requests
"""

import argparse
import base64
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_OWNER = "SpiralCloudOmega"
REPO_NAME = "PACKTPub_The_Digital_Library_Of_Alexandria"
API_BASE = "https://api.github.com"
BRANCH = "main"


def get_token(args_token: str) -> str:
    """Get GitHub token from args or environment."""
    token = args_token or os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print(
            "⚠️  No GitHub token provided. Set GITHUB_TOKEN env var or use --token.\n"
            "   You can create a token at: https://github.com/settings/tokens\n"
            "   Required scopes: repo (for private) or public_repo (for public)\n"
        )
    return token


def upload_file(
    local_path: str,
    dest_folder: str,
    filename: str,
    token: str,
    message: str,
    branch: str = BRANCH,
) -> bool:
    """Upload a local file to the repository."""
    try:
        import requests
    except ImportError:
        print("❌ Missing dependency: pip install requests")
        sys.exit(1)

    dest_folder = dest_folder.strip("/")
    remote_path = f"{dest_folder}/{filename}"

    print(f"📤 Uploading: {local_path} → {remote_path}")

    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("utf-8")

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{remote_path}"

    # Check if file already exists (to get its SHA for update)
    existing_sha = None
    check = requests.get(url, headers=headers)
    if check.status_code == 200:
        existing_sha = check.json().get("sha")
        print(f"   ℹ️  File already exists — will update (SHA: {existing_sha[:8]}...)")

    payload = {
        "message": message or f"Add {filename}",
        "content": content_b64,
        "branch": branch,
    }
    if existing_sha:
        payload["sha"] = existing_sha

    resp = requests.put(url, json=payload, headers=headers)

    if resp.status_code in (200, 201):
        action = "updated" if existing_sha else "created"
        file_url = resp.json()["content"]["html_url"]
        print(f"   ✅ Successfully {action}!")
        print(f"   🔗 {file_url}")
        return True
    else:
        print(f"   ❌ Upload failed: {resp.status_code} — {resp.json().get('message', '')}")
        return False


def download_and_upload(
    url: str,
    dest_folder: str,
    filename: str,
    token: str,
    message: str,
    branch: str = BRANCH,
) -> bool:
    """Download a file from URL and upload it to the repository."""
    if not filename:
        filename = url.split("/")[-1].split("?")[0]
        if not filename:
            print("❌ Could not determine filename from URL. Use --filename.")
            return False

    suffix = Path(filename).suffix or ""
    print(f"⬇️  Downloading: {url}")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
        urllib.request.urlretrieve(url, tmp_path)
        size_mb = os.path.getsize(tmp_path) / (1024 * 1024)
        print(f"   ✅ Downloaded ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
        return False

    result = upload_file(tmp_path, dest_folder, filename, token, message, branch)
    os.unlink(tmp_path)
    return result


def bulk_upload(folder: str, dest_folder: str, token: str, message: str) -> None:
    """Upload all documents from a local folder."""
    extensions = {
        ".pdf", ".epub", ".mobi", ".azw", ".azw3",
        ".pptx", ".ppt", ".key", ".odp",
        ".xlsx", ".xls", ".csv", ".ods",
        ".docx", ".doc", ".odt", ".rtf", ".txt",
    }
    files = [
        p for p in Path(folder).iterdir()
        if p.is_file() and p.suffix.lower() in extensions
    ]
    if not files:
        print(f"⚠️  No supported document files found in: {folder}")
        return

    print(f"📦 Bulk uploading {len(files)} file(s) from '{folder}' → '{dest_folder}'")
    success = 0
    for f in files:
        if upload_file(str(f), dest_folder, f.name, token, message or f"Add {f.name}"):
            success += 1
    print(f"\n✅ Uploaded {success}/{len(files)} files successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Quick upload documents to The Library of Alexandria",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Path to local file to upload")
    source.add_argument("--url", help="URL of file to download and upload")
    source.add_argument("--bulk", help="Path to local folder for bulk upload")

    parser.add_argument(
        "--dest",
        default="docs/Other",
        help="Destination folder in the repo (default: docs/Other)",
    )
    parser.add_argument("--filename", help="Override destination filename")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--message", help="Commit message")
    parser.add_argument("--branch", default=BRANCH, help=f"Target branch (default: {BRANCH})")

    args = parser.parse_args()
    token = get_token(args.token)

    if args.file:
        if not os.path.isfile(args.file):
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        filename = args.filename or Path(args.file).name
        success = upload_file(args.file, args.dest, filename, token, args.message, args.branch)
    elif args.url:
        success = download_and_upload(args.url, args.dest, args.filename, token, args.message, args.branch)
    elif args.bulk:
        bulk_upload(args.bulk, args.dest, token, args.message)
        return

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
