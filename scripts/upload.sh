#!/usr/bin/env bash
# Quick Upload Script for The Library of Alexandria
# ===================================================
# Upload a local file or download-then-upload from a URL.
#
# Usage:
#   ./upload.sh <file_path> [dest_folder] [commit_message]
#   ./upload.sh --url <url> [dest_folder] [filename] [commit_message]
#
# Environment variables:
#   GITHUB_TOKEN — Personal access token (required for push)
#
# Examples:
#   ./upload.sh mybook.pdf docs/PDFs "Add mybook.pdf"
#   ./upload.sh --url https://example.com/book.pdf docs/PDFs book.pdf "Add book.pdf"

set -euo pipefail

REPO_OWNER="SpiralCloudOmega"
REPO_NAME="PACKTPub_The_Digital_Library_Of_Alexandria"
BRANCH="${GITHUB_BRANCH:-main}"
TOKEN="${GITHUB_TOKEN:-}"
API_BASE="https://api.github.com"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

log_info()    { echo -e "${BLUE}ℹ️  $*${NC}"; }
log_success() { echo -e "${GREEN}✅ $*${NC}"; }
log_warn()    { echo -e "${YELLOW}⚠️  $*${NC}"; }
log_error()   { echo -e "${RED}❌ $*${NC}"; exit 1; }

require_cmd() { command -v "$1" >/dev/null 2>&1 || log_error "Required command not found: $1"; }
require_cmd curl
require_cmd base64
require_cmd python3

if [[ -z "$TOKEN" ]]; then
    log_warn "GITHUB_TOKEN not set. Uploads will fail without authentication."
    log_warn "Set it with: export GITHUB_TOKEN=your_token"
fi

# Track whether we're in URL mode (before any shifts)
URL_MODE=false

# ─── Download from URL mode ───────────────────────────────────────────────────
if [[ "${1:-}" == "--url" ]]; then
    URL_MODE=true
    shift
    URL="${1:?Usage: $0 --url <url> [dest_folder] [filename] [message]}"
    DEST="${2:-docs/Other}"
    FILENAME="${3:-$(basename "$URL" | cut -d'?' -f1)}"
    MESSAGE="${4:-Add $FILENAME}"

    TMP_FILE=$(mktemp)
    log_info "Downloading: $URL"
    curl -fsSL -o "$TMP_FILE" "$URL"
    SIZE=$(du -sh "$TMP_FILE" | cut -f1)
    log_success "Downloaded ($SIZE)"

    FILE="$TMP_FILE"
else
    # ─── Local file mode ──────────────────────────────────────────────────────
    FILE="${1:?Usage: $0 <file_path> [dest_folder] [commit_message]}"
    DEST="${2:-docs/Other}"
    MESSAGE="${3:-Add $(basename "$FILE")}"
    FILENAME="$(basename "$FILE")"
fi

[[ -f "$FILE" ]] || log_error "File not found: $FILE"

REMOTE_PATH="${DEST%/}/${FILENAME}"
log_info "Uploading: $FILE → $REMOTE_PATH"

# Encode file as base64
CONTENT_B64=$(base64 < "$FILE" | tr -d '\n')

# Check if file already exists
EXISTING_SHA=""
AUTH_HEADER=""
[[ -n "$TOKEN" ]] && AUTH_HEADER="Authorization: Bearer $TOKEN"

CHECK_URL="$API_BASE/repos/$REPO_OWNER/$REPO_NAME/contents/$REMOTE_PATH"
CHECK_RESP=$(mktemp)

if [[ -n "$TOKEN" ]]; then
    HTTP_CODE=$(curl -s -o "$CHECK_RESP" -w "%{http_code}" \
        -H "$AUTH_HEADER" \
        -H "Accept: application/vnd.github+json" \
        "$CHECK_URL")
else
    HTTP_CODE=$(curl -s -o "$CHECK_RESP" -w "%{http_code}" \
        -H "Accept: application/vnd.github+json" \
        "$CHECK_URL")
fi

if [[ "$HTTP_CODE" == "200" ]]; then
    EXISTING_SHA=$(python3 -c "import json, sys; print(json.load(open(sys.argv[1])).get('sha',''))" "$CHECK_RESP")
    log_info "File already exists — will update (SHA: ${EXISTING_SHA:0:8}...)"
fi
rm -f "$CHECK_RESP"

# Build JSON payload using environment variables to avoid shell injection
if [[ -n "$EXISTING_SHA" ]]; then
    PAYLOAD=$(MSG="$MESSAGE" CONTENT="$CONTENT_B64" BRANCH="$BRANCH" SHA="$EXISTING_SHA" python3 -c "
import json, os
print(json.dumps({
    'message': os.environ['MSG'],
    'content': os.environ['CONTENT'],
    'branch':  os.environ['BRANCH'],
    'sha':     os.environ['SHA'],
}))
")
else
    PAYLOAD=$(MSG="$MESSAGE" CONTENT="$CONTENT_B64" BRANCH="$BRANCH" python3 -c "
import json, os
print(json.dumps({
    'message': os.environ['MSG'],
    'content': os.environ['CONTENT'],
    'branch':  os.environ['BRANCH'],
}))
")
fi

# Upload
PUT_URL="$API_BASE/repos/$REPO_OWNER/$REPO_NAME/contents/$REMOTE_PATH"

if [[ -n "$TOKEN" ]]; then
    RESP=$(curl -s -w "\n%{http_code}" -X PUT \
        -H "$AUTH_HEADER" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$PAYLOAD" \
        "$PUT_URL")
else
    RESP=$(curl -s -w "\n%{http_code}" -X PUT \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$PAYLOAD" \
        "$PUT_URL")
fi

HTTP_STATUS=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | head -n -1)

if [[ "$HTTP_STATUS" == "200" || "$HTTP_STATUS" == "201" ]]; then
    FILE_URL=$(python3 -c "import json; print(json.loads('''$RESP_BODY''').get('content',{}).get('html_url',''))" 2>/dev/null || echo "")
    ACTION=$([[ "$HTTP_STATUS" == "201" ]] && echo "created" || echo "updated")
    log_success "Successfully $ACTION!"
    [[ -n "$FILE_URL" ]] && log_info "URL: $FILE_URL"
else
    ERROR=$(python3 -c "import json; print(json.loads('''$RESP_BODY''').get('message','Unknown error'))" 2>/dev/null || echo "Unknown error")
    log_error "Upload failed ($HTTP_STATUS): $ERROR"
fi

# Clean up temp file if we downloaded it
[[ "$URL_MODE" == "true" ]] && rm -f "$TMP_FILE"
