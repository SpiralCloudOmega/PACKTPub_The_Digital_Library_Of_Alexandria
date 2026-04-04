# 📖 The Library of Alexandria — PDF & Document Repository

> *"A place where all knowledge converges."*

A curated, community-friendly repository for storing and sharing PDFs, eBooks, presentations, spreadsheets, and all kinds of documents — along with a complete index of the **9,200+ PacktPublishing repositories**.

## 🚀 Launch the Web App

> **[▶ Open Library of Alexandria App](https://spiralcloudOmega.github.io/PACKTPub_The_Digital_Library_Of_Alexandria/)** ← GitHub Pages web app

The app is a **Filza File Manager-inspired** web interface with 4 built-in tools:

| Tab | What it does |
|-----|-------------|
| 📁 **Files** | Browse, upload & download files in this repo |
| 🔄 **Convert** | Convert documents to PDF, HTML, Markdown, EPUB, ODT, TXT, RTF |
| ✏️ **Editor** | Full text editor with **line numbers** + syntax highlighting |
| ⚙️ **Settings** | Set your GitHub token to enable uploads & saving |

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
└── generate_packt_index.py — Regenerate the PacktPublishing index

📁 .github/workflows/
├── update_packt_index.yml  — Auto-update Packt index (scheduled weekly)
└── quick_upload.yml        — Upload a document via GitHub Actions dispatch

📄 PACKT_INDEX.md    — Complete clickable index of all PacktPublishing repos
📄 CONTRIBUTING.md   — How to contribute documents
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

➡️ **[View the PacktPublishing Repository Index](PACKT_INDEX.md)**

The [`PACKT_INDEX.md`](PACKT_INDEX.md) is an alphabetically-organized, clickable index of repositories in the [PacktPublishing GitHub organization](https://github.com/PacktPublishing) — a gold mine of code samples, notebooks, and documentation for hundreds of technical books covering 9,200+ repos total.

> **Note:** The current index contains ~1,000 repositories fetched at setup time. Run the generator script or trigger the weekly workflow to regenerate the complete index of all 9,200+ repos.

### Regenerating the Index
The index is automatically updated weekly via GitHub Actions. To manually regenerate:

```bash
# With a GitHub token (recommended to avoid rate limits)
GITHUB_TOKEN=your_token python scripts/generate_packt_index.py

# Without a token (rate-limited to 60 requests/hour)
python scripts/generate_packt_index.py
```

Or trigger it from the Actions tab → **Update PacktPublishing Index** → **Run workflow**.

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
