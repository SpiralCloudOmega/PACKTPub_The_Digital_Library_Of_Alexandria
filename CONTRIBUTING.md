# Contributing to The Library of Alexandria

Thank you for helping grow the library! Here's how to add documents.

## 📁 Where to Put Files

| Document Type | Destination Folder |
|---------------|-------------------|
| PDFs | `docs/PDFs/` |
| eBooks (EPUB, MOBI) | `docs/eBooks/` |
| Presentations (PPTX, KEY) | `docs/Presentations/` |
| Spreadsheets (XLSX, CSV) | `docs/Spreadsheets/` |
| Everything else | `docs/Other/` |

## ✅ File Naming Convention

Use descriptive, hyphenated names without spaces:

```
Good:  python-data-science-handbook-2024.pdf
Good:  kubernetes-in-action-3rd-edition.epub
Bad:   My File (1).pdf
Bad:   scan0001.pdf
```

## 🚫 What NOT to Upload

- Copyrighted materials you don't have the right to distribute
- Executable files (`.exe`, `.bat`, `.sh` scripts containing malware)
- Personal or sensitive information

> **Large files are welcome!** This repo uses Git LFS — files of any size in `docs/` are handled automatically. Just make sure you have [Git LFS installed](https://git-lfs.github.com/) (`git lfs install`).

## 📤 Upload Methods

### Via GitHub Web UI
1. Navigate to the correct subfolder in `docs/`
2. Click **Add file → Upload files**
3. Drag & drop your files
4. Write a clear commit message: `Add <title> by <author>`
5. Click **Commit changes**

### Via Git CLI
```bash
git clone https://github.com/SpiralCloudOmega/PACKTPub_The_Digital_Library_Of_Alexandria.git
cd PACKTPub_The_Digital_Library_Of_Alexandria
cp ~/Downloads/mybook.pdf docs/PDFs/
git add .
git commit -m "Add mybook.pdf"
git push
```

### Via Python Upload Script
```bash
python scripts/upload.py --file mybook.pdf --dest docs/PDFs --message "Add mybook.pdf"
```

### Via GitHub Actions Workflow
Go to **Actions → Quick Upload Document → Run workflow** and provide:
- `file_url`: A public URL to the document (direct download link)
- `destination`: Target folder (e.g., `docs/PDFs`)
- `filename`: (Optional) override the filename

## 📝 Commit Message Format

```
Add <title> - <author/source>
Update <filename> - <reason>
Remove <filename> - <reason>
```

## 🙏 Code of Conduct

Be respectful. Only share documents you have the right to distribute.
