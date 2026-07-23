#!/usr/bin/env python3
"""Build standalone HTML note pages from Markdown files in notes/.

Usage:
    python3 build_notes.py

For each notes/*.md file this creates notes/<slug>.html styled to match the
site, and regenerates the Notes list on index.html (between the
<!-- NOTES:START --> and <!-- NOTES:END --> markers).

No third-party dependencies. Supports a common Markdown subset: headings,
bold/italic, inline code, fenced code blocks, links, blockquotes, unordered
and ordered lists, and paragraphs. Optional YAML-ish front matter
(title / date / summary) at the top of a file.
"""

import datetime
import html
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(ROOT, "notes")
INDEX = os.path.join(ROOT, "index.html")


# ---------------------------------------------------------------- front matter
def parse_front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end].strip("\n")
            for line in block.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip()
            text = text[end + 4:].lstrip("\n")
    return meta, text


# ---------------------------------------------------------------- math protect
# Math spans are pulled out BEFORE any Markdown/HTML processing and restored
# verbatim at the very end, so MathJax sees the original LaTeX untouched.
MATH_PLACEHOLDER = "\x01MATH%d\x01"


def protect_math(text, store):
    """Replace $$...$$ and $...$ with placeholders; keep LaTeX verbatim."""
    def repl_block(m):
        store.append(m.group(0))  # keep the $$ delimiters for MathJax
        return MATH_PLACEHOLDER % (len(store) - 1)

    def repl_inline(m):
        store.append(m.group(0))
        return MATH_PLACEHOLDER % (len(store) - 1)

    # $$ ... $$  (may span multiple lines)
    text = re.sub(r"\$\$.*?\$\$", repl_block, text, flags=re.DOTALL)
    # $ ... $  (single line, non-greedy, not empty, avoid $$ leftovers)
    text = re.sub(r"(?<!\$)\$(?!\s)(?:\\.|[^$\\\n])+?\$(?!\$)", repl_inline, text)
    return text


def restore_math(text, store):
    return re.sub(r"\x01MATH(\d+)\x01",
                  lambda m: store[int(m.group(1))], text)


# ---------------------------------------------------------------- inline md
def inline(text):
    """Escape HTML then apply inline Markdown. Code spans are protected."""
    spans = []

    def stash(m):
        spans.append(html.escape(m.group(1)))
        return "\x00%d\x00" % (len(spans) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)),
                  text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: "<code>%s</code>" % spans[int(m.group(1))], text)
    return text


# ---------------------------------------------------------------- block md
def render_markdown(text):
    math = []
    text = protect_math(text, math)

    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)

    def close_list(stack):
        while stack:
            out.append("</%s>" % stack.pop())

    list_stack = []  # tags currently open: 'ul' or 'ol'

    def is_table_sep(s):
        return bool(re.match(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$", s)) and "-" in s

    def split_row(s):
        s = s.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        return [c.strip() for c in s.split("|")]

    def strip_indent(s, amount):
        """Remove up to `amount` leading spaces (for dedenting code content)."""
        j = 0
        while j < amount and j < len(s) and s[j] == " ":
            j += 1
        return s[j:]

    # Block markers are matched after optional leading whitespace, so notes
    # authored as one big nested list (everything indented under a top-level
    # bullet — common when pasting from blog editors) still parse correctly.
    fence_re = re.compile(r"^(\s*)```(.*)$")
    heading_re = re.compile(r"^\s*(#{1,6})\s+(.*)")
    ul_re = re.compile(r"^\s*[-*+]\s+(.*)")
    ol_re = re.compile(r"^\s*\d+\.\s+(.*)")
    hr_re = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
    quote_re = re.compile(r"^\s*>\s?(.*)")
    marker_re = re.compile(r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|>|```|(-{3,}|\*{3,}|_{3,})\s*$)")

    while i < n:
        line = lines[i]

        # fenced code block (indent-tolerant; content dedented by fence indent)
        m = fence_re.match(line)
        if m:
            close_list(list_stack)
            indent = len(m.group(1))
            i += 1
            buf = []
            while i < n and not fence_re.match(lines[i]):
                buf.append(html.escape(strip_indent(lines[i], indent)))
                i += 1
            i += 1  # skip closing fence
            out.append("<pre><code>%s</code></pre>" % "\n".join(buf))
            continue

        # table: a header row followed by a |---|---| separator
        if "|" in line and i + 1 < n and is_table_sep(lines[i + 1]):
            close_list(list_stack)
            headers = split_row(line)
            i += 2  # skip header + separator
            body = []
            while i < n and "|" in lines[i] and lines[i].strip():
                body.append(split_row(lines[i]))
                i += 1
            thead = "".join("<th>%s</th>" % inline(h) for h in headers)
            rows = []
            for r in body:
                cells = "".join("<td>%s</td>" % inline(c) for c in r)
                rows.append("<tr>%s</tr>" % cells)
            out.append("<table class=\"md-table\"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
                       % (thead, "".join(rows)))
            continue

        # blank line
        if line.strip() == "":
            close_list(list_stack)
            i += 1
            continue

        # horizontal rule (before lists: '***'/'---' would also match a bullet)
        if hr_re.match(line):
            close_list(list_stack)
            out.append("<hr>")
            i += 1
            continue

        # heading
        m = heading_re.match(line)
        if m:
            close_list(list_stack)
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2).strip()), level))
            i += 1
            continue

        # blockquote
        if quote_re.match(line):
            close_list(list_stack)
            buf = []
            while i < n and quote_re.match(lines[i]):
                buf.append(inline(quote_re.match(lines[i]).group(1).strip()))
                i += 1
            out.append("<blockquote>%s</blockquote>" % "<br>".join(buf))
            continue

        # unordered list
        m = ul_re.match(line)
        if m:
            if not list_stack or list_stack[-1] != "ul":
                close_list(list_stack)
                out.append("<ul>")
                list_stack.append("ul")
            out.append("<li>%s</li>" % inline(m.group(1)))
            i += 1
            continue

        # ordered list
        m = ol_re.match(line)
        if m:
            if not list_stack or list_stack[-1] != "ol":
                close_list(list_stack)
                out.append("<ol>")
                list_stack.append("ol")
            out.append("<li>%s</li>" % inline(m.group(1)))
            i += 1
            continue

        # paragraph (gather consecutive non-blank, non-special lines)
        close_list(list_stack)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() != "" and "|" not in lines[i] \
                and not marker_re.match(lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf).strip()))

    close_list(list_stack)
    return restore_math("\n".join(out), math)


# ---------------------------------------------------------------- page template
# NOTE: built with str.replace (not .format) because note bodies contain
# LaTeX braces { } that would break .format().
PAGE = r"""<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>@@TITLE@@ · Akuiro</title>
    <meta name="author" content="Akuiro / Zhenkui Zhou">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="../images/favicon/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="../stylesheet.css">
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true,
          tags: 'ams'
        },
        options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  </head>
  <body>
    <table class="page"><tbody>
      <tr>
        <td style="padding:2.5%">
          <p class="note-nav"><a href="../index.html">← Akuiro</a></p>
          <article class="note">
            <h1 class="note-title">@@TITLE@@</h1>
            @@DATE@@
            @@BODY@@
          </article>
          <p class="note-nav" style="margin-top:32px;"><a href="../index.html">← Back home</a></p>
        </td>
      </tr>
    </tbody></table>
  </body>
</html>
"""


def slugify(name):
    """Filesystem-safe slug that keeps Unicode (e.g. Chinese) intact.

    Only characters unsafe in a path/URL are replaced; CJK filenames stay
    readable and unique instead of collapsing to identical dashes.
    """
    base = os.path.splitext(os.path.basename(name))[0].strip()
    base = re.sub(r"\s+", "-", base)
    base = re.sub(r'[\\/:*?"<>|#%]+', "-", base)  # unsafe in fs/url
    base = base.strip("-") or "note"
    return base


def auto_summary(text, limit=70):
    """First meaningful prose line of the body, for the homepage list."""
    in_code = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not s or s == "---":
            continue
        # skip headings, table rows, and table-of-contents entries
        if s.startswith("#") or s.startswith("|") or "](#" in s or re.match(r"^\d+\.\s*\[", s):
            continue
        s = s.lstrip(">*-+ ").strip()             # strip leading markers
        if not s:
            continue
        s = re.sub(r"\$[^$]*\$", "", s)            # drop inline math
        s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)  # links -> text
        s = re.sub(r"~~([^~]*)~~", r"\1", s)       # strikethrough
        s = re.sub(r"[*`_#]", "", s).strip()       # drop remaining md markers
        if len(s) >= 6:
            return s[:limit] + ("…" if len(s) > limit else "")
    return ""


def build_note(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    meta, text = parse_front_matter(raw)
    # title: front matter > original filename (no extension)
    title = meta.get("title") or os.path.splitext(os.path.basename(path))[0].strip()
    # date: front matter > file modification date (hybrid mode)
    date = meta.get("date", "")
    if not date:
        date = datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    summary = meta.get("summary", "") or auto_summary(text)
    datehtml = '<p class="note-date">%s</p>' % html.escape(date) if date else ""
    body = render_markdown(text)
    page = (PAGE
            .replace("@@TITLE@@", html.escape(title))
            .replace("@@DATE@@", datehtml)
            .replace("@@BODY@@", body))
    slug = slugify(path)
    out_path = os.path.join(NOTES_DIR, slug + ".html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    href = "notes/" + urllib.parse.quote(slug + ".html")
    return {"title": title, "date": date, "summary": summary, "href": href}


# ---------------------------------------------------------------- homepage list
def render_list(notes):
    if not notes:
        return '<p class="item-meta">No notes yet.</p>'
    rows = []
    for note in notes:
        meta = " · ".join(x for x in [note["date"], note["summary"]] if x)
        rows.append(
            '<li><a href="%s">%s</a>%s</li>' % (
                note["href"], html.escape(note["title"]),
                (' <span class="note-meta">%s</span>' % html.escape(meta)) if meta else ""))
    return '<ul class="cv-list note-list">\n' + "\n".join(rows) + "\n</ul>"


def update_index(notes):
    with open(INDEX, encoding="utf-8") as f:
        page = f.read()
    start = "<!-- NOTES:START -->"
    end = "<!-- NOTES:END -->"
    if start not in page or end not in page:
        print("warning: NOTES markers not found in index.html; skipping list update")
        return
    new = page[:page.index(start) + len(start)] + "\n" + render_list(notes) + "\n" + \
        " " * 16 + page[page.index(end):]
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new)


def main():
    if not os.path.isdir(NOTES_DIR):
        print("no notes/ directory found")
        return
    md_files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith(".md"))
    notes = [build_note(os.path.join(NOTES_DIR, f)) for f in md_files]
    # newest first (front-matter date, else filename)
    notes.sort(key=lambda note: note["date"] or "", reverse=True)
    update_index(notes)
    print("built %d note(s):" % len(notes))
    for note in notes:
        print("  -", note["href"])


if __name__ == "__main__":
    sys.exit(main())
