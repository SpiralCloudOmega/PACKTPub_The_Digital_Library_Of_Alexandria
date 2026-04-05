# 📖 The Library of Alexandria — PDF & Document Repository

> *"A place where all knowledge converges."*

A curated, community-friendly repository for storing and sharing PDFs, eBooks, presentations, spreadsheets, and all kinds of documents — along with a complete index of the **9,200+ PacktPublishing repositories**.

## 🚀 Launch the Web App

> **[▶ Open Library of Alexandria App](https://spiralcloudOmega.github.io/PACKTPub_The_Digital_Library_Of_Alexandria/)** ← GitHub Pages web app

The app is a **Filza File Manager-inspired** web interface with 5 built-in tools:

| Tab | What it does |
|-----|-------------|
| 📁 **Files** | Browse, upload & download files in this repo |
| 🔄 **Convert** | Convert documents to PDF, HTML, Markdown, EPUB, ODT, TXT, RTF |
| ✏️ **Editor** | Full text editor with **line numbers** + syntax highlighting |
| ⚙️ **Settings** | Set your GitHub token to enable uploads & saving |
| 📚 **Packt** | Search & browse all 9,200+ PacktPublishing repos with filters |

> **First time?** Go to ⚙️ Settings → paste your [GitHub Personal Access Token](https://github.com/settings/tokens) (needs `repo` scope) → start uploading.

[![Deploy to GitHub Pages](https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria/actions/workflows/pages.yml/badge.svg)](https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria/actions/workflows/pages.yml)
[![Update PacktPublishing Index](https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria/actions/workflows/update_packt_index.yml/badge.svg)](https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria/actions/workflows/update_packt_index.yml)

---

## 📂 Repository Structure

```
📁 docs/
├── 📄 PDFs/           — PDF documents
├── 📗 eBooks/         — eBooks (EPUB, MOBI, PDF)
├── 📊 Presentations/  — Slides & presentations (PPTX, KEY, PDF)
├── 📈 Spreadsheets/   — Data files (XLSX, CSV, ODS)
└── 📎 Other/          — Any other document types

📁 scripts/
├── upload.py               — Python quick-upload helper
├── upload.sh               — Shell quick-upload helper
├── generate_packt_index.py — Regenerate the PacktPublishing index
└── packt_stats.py          — Index statistics & topic categorizer

📁 .github/workflows/
├── pages.yml               — Deploy web app to GitHub Pages
├── update_packt_index.yml  — Auto-update Packt index (weekly)
├── quick_upload.yml        — Upload a document via GitHub Actions dispatch
├── auto-merge.yml          — Auto-merge Copilot agent PRs
└── health-check.yml        — Weekly repo health & integrity check

📄 PACKT_INDEX.md    — Complete clickable index of all PacktPublishing repos
📄 PACKT_TOPICS.md   — Topic-organized view (AI/ML, Web Dev, DevOps, etc.)
📄 CONTRIBUTING.md   — How to contribute documents
📄 .gitattributes    — Git LFS tracking for large documents
```

---

## 🚀 Quick Upload Options

### Option 1 — GitHub Web UI (No tools needed)
1. Navigate to the correct folder (e.g., `docs/PDFs/`)
2. Click **Add file → Upload files**
3. Drag and drop your document(s)
4. Add a commit message and click **Commit changes**

### Option 2 — Python Upload Script
```bash
# Install dependencies
pip install requests

# Upload a single file
python scripts/upload.py --file mybook.pdf --dest docs/PDFs --message "Add mybook.pdf"

# Upload with a token (for private repos)
python scripts/upload.py --file mybook.pdf --dest docs/PDFs --token YOUR_GITHUB_TOKEN
```

### Option 3 — Shell Upload Script
```bash
# Make executable
chmod +x scripts/upload.sh

# Upload a file
./scripts/upload.sh mybook.pdf docs/PDFs "Add mybook.pdf"
```

### Option 4 — GitHub Actions Workflow Dispatch
1. Go to the **Actions** tab
2. Select **Quick Upload Document**
3. Click **Run workflow**
4. Fill in the file URL and destination folder
5. Click **Run workflow** — the document is downloaded and committed automatically

### Option 5 — Git Command Line
```bash
git clone https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria.git
cd PACKTPub_The_Digital_Library_Of_Alexandria
cp /path/to/your/file.pdf docs/PDFs/
git add docs/PDFs/file.pdf
git commit -m "Add file.pdf"
git push
```

---

## 📚 PacktPublishing Index

➡️ **[View the PacktPublishing Repository Index](PACKT_INDEX.md)** — 9,200+ repos, alphabetically organized
➡️ **[View by Topic](PACKT_TOPICS.md)** — categorized by AI/ML, Web Dev, Cloud, Security, and more

The [`PACKT_INDEX.md`](PACKT_INDEX.md) is an alphabetically-organized, clickable index of repositories in the [PacktPublishing GitHub organization](https://github.com/PacktPublishing) — a gold mine of code samples, notebooks, and documentation for hundreds of technical books covering 9,200+ repos total.

The [`PACKT_TOPICS.md`](PACKT_TOPICS.md) groups the same repos by **technology topic** — 18 categories with highlights, stats, and expandable full lists. Generated from the index by the stats script.

### Regenerating the Index
The index is automatically updated weekly via GitHub Actions. To manually regenerate:

```bash
# With a GitHub token (recommended to avoid rate limits)
GITHUB_TOKEN=your_token python scripts/generate_packt_index.py

# Without a token (rate-limited to 60 requests/hour)
python scripts/generate_packt_index.py
```

Or trigger it from the Actions tab → **Update PacktPublishing Index** → **Run workflow**.

### Generating Stats & Topics

```bash
# Print statistics to console
python scripts/packt_stats.py

# Generate PACKT_TOPICS.md (repos grouped by technology area)
python scripts/packt_stats.py --topics

# Export stats as JSON
python scripts/packt_stats.py --json
```

---

## 📦 Git LFS — Large File Support

This repo uses [Git LFS](https://git-lfs.github.com/) to handle documents larger than GitHub's 100 MB file size limit. All document types in `docs/` are tracked by default.

### Setup
```bash
# Install Git LFS (one-time)
git lfs install

# Clone the repo (LFS files download automatically)
git clone https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria.git
```

### Uploading Large Files (200 MB+)
```bash
# Files in docs/ are automatically tracked by LFS via .gitattributes
cp ~/Downloads/massive-book-500mb.pdf docs/PDFs/
git add docs/PDFs/massive-book-500mb.pdf
git commit -m "Add massive-book-500mb.pdf"
git push
```

> **No size limit worries** — LFS handles files of any size. The `.gitattributes` file automatically tracks PDFs, EPUBs, Office docs, archives, and more.

---

## 📋 Supported Document Types

| Type | Extensions | Folder |
|------|-----------|--------|
| PDF Documents | `.pdf` | `docs/PDFs/` |
| eBooks | `.epub`, `.mobi`, `.azw`, `.pdf` | `docs/eBooks/` |
| Presentations | `.pptx`, `.ppt`, `.key`, `.odp`, `.pdf` | `docs/Presentations/` |
| Spreadsheets | `.xlsx`, `.xls`, `.csv`, `.ods` | `docs/Spreadsheets/` |
| Word Documents | `.docx`, `.doc`, `.odt`, `.rtf` | `docs/Other/` |
| Other | `.txt`, `.md`, `.html`, `.zip` | `docs/Other/` |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to add documents to this repository.

---

## 📜 License

This repository is licensed under the [MIT License](LICENSE). Documents contributed here remain under their original licenses.
