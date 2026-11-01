# Akuiro (周朕葵) · Personal Homepage

[English](README.md) · [简体中文](README.zh-CN.md)

A personal homepage and lightweight notes system deployed on GitHub Pages.

🔗 Live site: <https://APhysickui.github.io/>

This is a static site. The homepage presents education, research, projects, and honors, alongside a **Markdown notes system**. Add `.md` files to `notes/` and run a script to generate standalone articles with equations and tables, and update the homepage Notes list automatically.

---

## Credits and source

The homepage layout and `stylesheet.css` are adapted from **Jon Barron's** academic homepage template: <https://jonbarron.info/>. The original README is available in Git history. This project extends its simple table-based layout with Chinese localization, responsive images, and a notes system.

## Features

- **Bilingual layout:** section headings combine English with a small Chinese label, such as `Research 科研经历`.
- **Responsive images:** CSS `aspect-ratio` and `object-fit: cover` handle cropping without fixed image dimensions. The portrait is circular, while project images use a 3:2 ratio. **Replace an image file directly; no manual cropping is needed.**
- **Mobile layout:** portraits, project images, and text stack into a single column on narrow screens; see `@media (max-width: 600px)` in `stylesheet.css`.
- **Markdown notes (`build_notes.py`):**
  - MathJax renders LaTeX math: inline `$...$`, display `$$...$$`, and `\begin{}` environments.
  - Tables, code blocks, blockquotes, ordered/unordered lists, and horizontal rules.
  - Chinese filenames with automatically URL-encoded links.
  - An automatically generated homepage Notes list, with extracted summaries and newest-first dates.
  - No third-party Python dependencies.

## Structure

```text
.
├── index.html          # Handwritten homepage; Notes list is injected by the script
├── stylesheet.css      # Site and note styles, adapted from Jon Barron's template
├── build_notes.py      # Markdown-to-HTML builder
├── notes/
│   ├── *.md            # Markdown source files you write
│   └── *.html          # Generated pages; do not edit manually
├── images/             # Portrait, project images, and favicon
├── data/               # CV in PDF / TeX form
├── .nojekyll           # Disable Jekyll processing for this static site
└── .gitignore
```

## Add a note

1. Create a `.md` file in `notes/`. Chinese filenames are supported and become the default article title.
2. Run:
   ```bash
   python3 build_notes.py
   ```
3. Check the output, then stage, commit, and push it.

The script generates a same-name `.html` page for each Markdown file and rebuilds the list between `<!-- NOTES:START -->` and `<!-- NOTES:END -->` in `index.html`. **Write the Markdown; the rest is automatic.**

### Optional title, date, and summary

Add front matter to the top of a note. Without it, the filename is used as the title, the file modification date as the date, and the first body sentence as the summary.

```markdown
---
title: A custom title
date: 2026-07-20
summary: A one-sentence introduction for the homepage list
---

The article starts here.
```

## Maintain personal information

Homepage information was synchronized with the latest academic CV and application materials on 2026-10-25 while retaining the existing layout and styling. `data/Zhenkui-Zhou-CV.pdf` is the supplied academic CV. `data/Zhenkui-Zhou-CV.tex` is a separately maintained extended version, not the source that generated that PDF.

When updating the site, keep the biography, email, research progress, graduation date, honors, and public CV consistent.

## Local preview

Serve the repository root locally so paths and navigation behave like the deployed site:

```bash
python3 -m http.server 8000
# Open http://localhost:8000/ in your browser
```

Opening HTML files directly with `file://` is discouraged because relative stylesheet paths may fail. MathJax loads from a CDN, so equation previews require network access.

## Deploy to GitHub Pages

The repository is named `APhysickui.github.io`, making it a GitHub Pages user site. Pushing to `main` publishes the repository root at <https://APhysickui.github.io/>.

Before deploying, run `python3 build_notes.py` locally and commit both the latest `notes/*.html` files and updated `index.html`. Generated HTML is version-controlled; GitHub Pages does not build these notes for you.

## Supported Markdown

| Syntax | Support |
| --- | --- |
| Headings `#`–`######` | ✅ |
| **Bold**, *italic*, and `inline code` | ✅ |
| Fenced code blocks | ✅ |
| Ordered / unordered lists | ✅ |
| Tables | ✅ |
| Blockquotes `>` | ✅ |
| Horizontal rules `---` | ✅ |
| Links `[text](url)` | ✅ |
| LaTeX `$...$` / `$$...$$` | ✅ MathJax |
| Images `![]()` / nested lists | ⚠️ Not supported yet |

## License

The homepage template belongs to its original author, Jon Barron. Personal content, including the biography, notes, and CV, is copyright 周朕葵 (Zhenkui Zhou).
