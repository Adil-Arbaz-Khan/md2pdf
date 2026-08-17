#!/usr/bin/env python3
"""
md2pdf — Zero-Dependency Markdown to PDF Converter
==================================================
Transforms Markdown documents into beautifully styled, print-ready PDF files
using the local headless Chromium/Edge browser engine already present on your system.

Author: Adil Arbaz Khan (https://github.com/Adil-Arbaz-Khan)
License: MIT
"""

import os
import sys
import re
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path

__version__ = "1.0.1"

# ----------------------------------------------------------------------
# CSS Design Themes
# ----------------------------------------------------------------------

DEFAULT_THEME = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* {
  box-sizing: border-box;
}

body {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #1e293b;
  background-color: #ffffff;
  line-height: 1.65;
  font-size: 13px;
  margin: 0;
  padding: 0;
}

h1 {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 8px;
  margin-top: 0;
  margin-bottom: 14px;
  letter-spacing: -0.02em;
}

h2 {
  font-size: 16.5px;
  font-weight: 700;
  color: #1e293b;
  border-bottom: 1px solid #cbd5e1;
  padding-bottom: 5px;
  margin-top: 24px;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
  page-break-after: avoid;
}

h3 {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin-top: 16px;
  margin-bottom: 6px;
  page-break-after: avoid;
}

h4, h5, h6 {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-top: 12px;
  margin-bottom: 4px;
  page-break-after: avoid;
}

p {
  margin: 6px 0 10px 0;
  color: #334155;
}

hr {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 20px 0;
}

ul, ol {
  margin: 6px 0 12px 22px;
  padding: 0;
}

li {
  margin-bottom: 4px;
  color: #334155;
}

code {
  font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
  font-size: 11.5px;
  background-color: #f1f5f9;
  color: #0f172a;
  padding: 2px 5px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

kbd {
  display: inline-block;
  padding: 1.5px 5.5px;
  font-family: 'JetBrains Mono', 'Consolas', monospace;
  font-size: 11px;
  font-weight: 600;
  line-height: 1.2;
  color: #1e293b;
  background-color: #f8fafc;
  border: 1px solid #cbd5e1;
  border-bottom: 2px solid #94a3b8;
  border-radius: 4px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.08);
  vertical-align: middle;
}

.math-inline {
  font-family: 'Times New Roman', 'Cambria Math', Georgia, serif;
  font-style: italic;
  padding: 0 2px;
  color: #0f172a;
}

pre.code-block {
  background-color: #0f172a;
  border-radius: 6px;
  padding: 12px 14px;
  overflow-x: auto;
  margin: 8px 0 14px 0;
  page-break-inside: avoid;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.2);
}

pre.code-block code {
  background-color: transparent;
  color: #f8fafc;
  border: none;
  padding: 0;
  font-size: 11.5px;
  line-height: 1.48;
  display: block;
  white-space: pre-wrap;
  word-break: break-all;
}

.table-container {
  margin: 12px 0 16px 0;
  page-break-inside: avoid;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  text-align: left;
}

th {
  background-color: #f8fafc;
  color: #0f172a;
  font-weight: 600;
  border: 1px solid #cbd5e1;
  padding: 7px 10px;
}

td {
  border: 1px solid #e2e8f0;
  padding: 6px 10px;
  vertical-align: top;
}

tr:nth-child(even) td {
  background-color: #f8fafc;
}

blockquote {
  margin: 10px 0;
  padding: 8px 14px;
  border-left: 4px solid #3b82f6;
  background-color: #f8fafc;
  color: #475569;
  border-radius: 0 4px 4px 0;
  page-break-inside: avoid;
}

blockquote p {
  margin: 0;
}

.callout {
  margin: 12px 0;
  padding: 10px 14px;
  border-left: 4px solid #3b82f6;
  border-radius: 4px;
  background-color: #f0fdf4;
  page-break-inside: avoid;
}

.callout-note { border-color: #3b82f6; background-color: #eff6ff; }
.callout-tip { border-color: #10b981; background-color: #ecfdf5; }
.callout-important { border-color: #8b5cf6; background-color: #f5f3ff; }
.callout-warning { border-color: #f59e0b; background-color: #fffbeb; }
.callout-caution { border-color: #ef4444; background-color: #fef2f2; }

.callout-title {
  font-weight: 700;
  font-size: 12px;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.callout-note .callout-title { color: #1d4ed8; }
.callout-tip .callout-title { color: #047857; }
.callout-important .callout-title { color: #6d28d9; }
.callout-warning .callout-title { color: #b45309; }
.callout-caution .callout-title { color: #b91c1c; }

a {
  color: #2563eb;
  text-decoration: none;
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.page-break {
  page-break-before: always;
}
"""

DARK_THEME = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; }

body {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #e2e8f0;
  background-color: #0f172a;
  line-height: 1.65;
  font-size: 13px;
  margin: 0;
  padding: 0;
}

h1 { font-size: 22px; color: #f8fafc; border-bottom: 2px solid #334155; padding-bottom: 8px; margin: 0 0 14px 0; }
h2 { font-size: 16.5px; color: #f1f5f9; border-bottom: 1px solid #334155; padding-bottom: 5px; margin: 24px 0 10px 0; page-break-after: avoid; }
h3 { font-size: 14px; color: #cbd5e1; margin: 16px 0 6px 0; page-break-after: avoid; }
h4, h5, h6 { font-size: 13px; color: #94a3b8; margin: 12px 0 4px 0; page-break-after: avoid; }
p, li { color: #cbd5e1; margin: 6px 0 10px 0; }
hr { border: none; border-top: 1px solid #334155; margin: 20px 0; }
ul, ol { margin: 6px 0 12px 22px; padding: 0; }
li { margin-bottom: 4px; }

code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11.5px;
  background-color: #1e293b;
  color: #38bdf8;
  padding: 2px 5px;
  border-radius: 4px;
  border: 1px solid #334155;
}

kbd {
  display: inline-block;
  padding: 1.5px 5.5px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  line-height: 1.2;
  color: #f1f5f9;
  background-color: #1e293b;
  border: 1px solid #475569;
  border-bottom: 2px solid #64748b;
  border-radius: 4px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.3);
  vertical-align: middle;
}

.math-inline {
  font-family: 'Times New Roman', 'Cambria Math', Georgia, serif;
  font-style: italic;
  color: #38bdf8;
  padding: 0 2px;
}

pre.code-block {
  background-color: #020617;
  border-radius: 6px;
  padding: 12px 14px;
  overflow-x: auto;
  margin: 8px 0 14px 0;
  border: 1px solid #1e293b;
  page-break-inside: avoid;
}

pre.code-block code {
  background-color: transparent;
  color: #e2e8f0;
  border: none;
  padding: 0;
  font-size: 11.5px;
  line-height: 1.48;
  display: block;
  white-space: pre-wrap;
  word-break: break-all;
}

.table-container { margin: 12px 0 16px 0; page-break-inside: avoid; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { background-color: #1e293b; color: #f8fafc; font-weight: 600; border: 1px solid #334155; padding: 7px 10px; }
td { border: 1px solid #334155; padding: 6px 10px; color: #cbd5e1; }
tr:nth-child(even) td { background-color: #1e293b; }

blockquote {
  margin: 10px 0;
  padding: 8px 14px;
  border-left: 4px solid #38bdf8;
  background-color: #1e293b;
  color: #94a3b8;
  border-radius: 0 4px 4px 0;
}

.callout { margin: 12px 0; padding: 10px 14px; border-left: 4px solid #38bdf8; border-radius: 4px; background-color: #1e293b; }
.callout-note { border-color: #38bdf8; background-color: #0c4a6e; }
.callout-tip { border-color: #34d399; background-color: #064e3b; }
.callout-important { border-color: #a78bfa; background-color: #4c1d95; }
.callout-warning { border-color: #fbbf24; background-color: #78350f; }
.callout-caution { border-color: #f87171; background-color: #7f1d1d; }
.callout-title { font-weight: 700; font-size: 12px; margin-bottom: 4px; text-transform: uppercase; color: #f8fafc; }

a { color: #38bdf8; }
.page-break { page-break-before: always; }
"""

ACADEMIC_THEME = """
@page { margin: 20mm 20mm 20mm 20mm; }
* { box-sizing: border-box; }
body {
  font-family: 'Times New Roman', Times, Georgia, serif;
  color: #111111;
  background-color: #ffffff;
  line-height: 1.6;
  font-size: 12pt;
  margin: 0;
}
h1 { font-size: 18pt; font-weight: bold; text-align: center; margin-bottom: 18pt; border-bottom: 1px solid #111; padding-bottom: 6pt; }
h2 { font-size: 14pt; font-weight: bold; margin-top: 16pt; margin-bottom: 6pt; border-bottom: 0.5pt solid #888; page-break-after: avoid; }
h3 { font-size: 12pt; font-weight: bold; margin-top: 12pt; margin-bottom: 4pt; page-break-after: avoid; }
p, li { text-align: justify; margin: 4pt 0 6pt 0; }
code { font-family: 'Courier New', monospace; font-size: 10pt; background: #f4f4f4; padding: 1pt 3pt; border: 0.5pt solid #ddd; }
kbd { font-family: 'Courier New', monospace; font-size: 9.5pt; border: 1pt solid #444; padding: 1pt 4pt; background: #f9f9f9; }
.math-inline { font-style: italic; font-family: 'Times New Roman', serif; }
pre.code-block { background: #f8f8f8; border: 1pt solid #ccc; padding: 8pt; font-size: 9.5pt; margin: 8pt 0; page-break-inside: avoid; }
pre.code-block code { background: transparent; border: none; padding: 0; }
table { width: 100%; border-collapse: collapse; margin: 12pt 0; font-size: 10pt; page-break-inside: avoid; }
th { border-top: 1.5pt solid #111; border-bottom: 1pt solid #111; padding: 4pt 6pt; text-align: left; }
td { border-bottom: 0.5pt solid #ddd; padding: 4pt 6pt; }
blockquote { border-left: 2pt solid #666; margin: 8pt 0 8pt 16pt; padding-left: 8pt; font-style: italic; }
.page-break { page-break-before: always; }
"""

THEMES = {
    "default": DEFAULT_THEME,
    "dark": DARK_THEME,
    "academic": ACADEMIC_THEME
}

# ----------------------------------------------------------------------
# Math & Special Symbols Mapping
# ----------------------------------------------------------------------

MATH_SYMBOLS = {
    r'\rightarrow': '&rarr;',
    r'\leftarrow': '&larr;',
    r'\leftrightarrow': '&harr;',
    r'\Rightarrow': '&rArr;',
    r'\Leftarrow': '&lArr;',
    r'\Leftrightarrow': '&hArr;',
    r'\to': '&rarr;',
    r'\approx': '&asymp;',
    r'\sim': '&sim;',
    r'\neq': '&ne;',
    r'\ne': '&ne;',
    r'\le': '&le;',
    r'\leq': '&le;',
    r'\ge': '&ge;',
    r'\geq': '&ge;',
    r'\pm': '&plusmn;',
    r'\times': '&times;',
    r'\div': '&divide;',
    r'\cdot': '&middot;',
    r'\dots': '&hellip;',
    r'\ldots': '&hellip;',
    r'\cdots': '&hellip;',
    r'\infty': '&infin;',
    r'\sum': '&sum;',
    r'\prod': '&prod;',
    r'\partial': '&part;',
    r'\alpha': '&alpha;',
    r'\beta': '&beta;',
    r'\gamma': '&gamma;',
    r'\delta': '&delta;',
    r'\theta': '&theta;',
    r'\lambda': '&lambda;',
    r'\mu': '&mu;',
    r'\pi': '&pi;',
    r'\sigma': '&sigma;',
    r'\omega': '&omega;',
    r'\degree': '&deg;',
    r'^\circ': '&deg;',
}

SAFE_INLINE_TAGS = [
    'kbd', 'sub', 'sup', 'mark', 'span', 'b', 'i', 'u',
    'strong', 'em', 'del', 'code', 'small', 'abbr', 'wbr', 'br', 'hr'
]

# ----------------------------------------------------------------------
# Markdown Parser Engine
# ----------------------------------------------------------------------

def inline_format(text: str) -> str:
    # 1. Escape basic HTML entities
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 2. Restore allowed safe inline HTML tags (like <kbd>, <sub>, <sup>, etc.)
    for tag in SAFE_INLINE_TAGS:
        # Standard closing tags </tag>
        text = re.sub(rf'&lt;/{tag}&gt;', f'</{tag}>', text, flags=re.IGNORECASE)
        # Self closing <tag/> or <tag>
        text = re.sub(rf'&lt;{tag}\s*/?&gt;', f'<{tag}>', text, flags=re.IGNORECASE)
        # Tags with attributes <tag class="...">
        text = re.sub(rf'&lt;({tag}\s+[^&gt;]+)&gt;', r'<\1>', text, flags=re.IGNORECASE)
    
    # 3. Parse LaTeX math / arrow expressions: $\rightarrow$ or $x \approx y$
    def replace_math_block(match):
        content = match.group(1).strip()
        for symbol, replacement in MATH_SYMBOLS.items():
            content = content.replace(symbol, replacement)
        return f"<span class='math-inline'>{content}</span>"

    text = re.sub(r'\$([^\$]+)\$', replace_math_block, text)

    # 4. Also replace standalone LaTeX symbols outside math delimiters
    for symbol, replacement in MATH_SYMBOLS.items():
        text = text.replace(symbol, replacement)

    # 5. Images: ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1" />', text)
    # 6. Inline code: `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 7. Bold italic: ***text*** or ___text___
    text = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'___([^_]+)___', r'<strong><em>\1</em></strong>', text)
    # 8. Bold: **text** or __text__
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
    # 9. Italic: *text* or _text_
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'<em>\1</em>', text)
    # 10. Strikethrough: ~~text~~
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
    # 11. Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

def parse_markdown(md_content: str) -> str:
    lines = md_content.splitlines()
    html_lines = []
    
    in_code_block = False
    code_lang = ""
    code_content = []
    
    in_table = False
    in_ul = False
    in_ol = False
    in_blockquote = False
    in_callout = False
    callout_type = ""
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Code blocks
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_text = "\n".join(code_content)
                code_text = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                html_lines.append(f"<pre class='code-block'><code class='lang-{code_lang}'>{code_text}</code></pre>")
                code_content = []
            else:
                if in_ul: html_lines.append("</ul>"); in_ul = False
                if in_ol: html_lines.append("</ol>"); in_ol = False
                if in_table: html_lines.append("</tbody></table></div>"); in_table = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                if in_callout: html_lines.append("</div>"); in_callout = False
                
                in_code_block = True
                code_lang = stripped[3:].strip()
            continue
            
        if in_code_block:
            code_content.append(line)
            continue
            
        # 2. Page Break Directive
        if stripped in ["\\pagebreak", "<!-- pagebreak -->", "<div class=\"page-break\"></div>"]:
            html_lines.append("<div class='page-break'></div>")
            continue
            
        # 3. Callout Boxes (> [!NOTE], > [!TIP], > [!IMPORTANT], > [!WARNING], > [!CAUTION])
        callout_match = re.match(r'^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', stripped, re.IGNORECASE)
        if callout_match:
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            if in_table: html_lines.append("</tbody></table></div>"); in_table = False
            if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
            if in_callout: html_lines.append("</div>"); in_callout = False
            
            callout_type = callout_match.group(1).lower()
            in_callout = True
            html_lines.append(f"<div class='callout callout-{callout_type}'><div class='callout-title'>{callout_type}</div>")
            continue
            
        # 4. Blockquotes
        if stripped.startswith(">"):
            quote_text = stripped[1:].strip()
            if in_callout:
                html_lines.append(f"<p>{inline_format(quote_text)}</p>")
                continue
            if not in_blockquote:
                in_blockquote = True
                html_lines.append("<blockquote>")
            html_lines.append(f"<p>{inline_format(quote_text)}</p>")
            continue
        else:
            if in_blockquote:
                html_lines.append("</blockquote>")
                in_blockquote = False
            if in_callout:
                html_lines.append("</div>")
                in_callout = False

        # 5. Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            parts = [p.strip() for p in stripped[1:-1].split("|")]
            
            # Header separator row: |:---|:---:|---:|
            if all(re.match(r"^:?-+:?$", p) for p in parts if p):
                continue
                
            if not in_table:
                in_table = True
                html_lines.append("<div class='table-container'><table><thead><tr>")
                for p in parts:
                    html_lines.append(f"<th>{inline_format(p)}</th>")
                html_lines.append("</tr></thead><tbody>")
            else:
                html_lines.append("<tr>")
                for p in parts:
                    html_lines.append(f"<td>{inline_format(p)}</td>")
                html_lines.append("</tr>")
            continue
        else:
            if in_table:
                html_lines.append("</tbody></table></div>")
                in_table = False

        # 6. Unordered Lists
        if re.match(r"^[\*\-\+]\s+", stripped):
            if in_ol: html_lines.append("</ol>"); in_ol = False
            if not in_ul:
                in_ul = True
                html_lines.append("<ul>")
            item_text = re.sub(r"^[\*\-\+]\s+", "", stripped)
            # Checkbox support
            if item_text.startswith("[ ] "):
                item_text = f"<input type='checkbox' disabled /> {item_text[4:]}"
            elif item_text.startswith("[x] ") or item_text.startswith("[X] "):
                item_text = f"<input type='checkbox' checked disabled /> {item_text[4:]}"
            html_lines.append(f"<li>{inline_format(item_text)}</li>")
            continue
        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False

        # 7. Ordered Lists
        if re.match(r"^\d+\.\s+", stripped):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if not in_ol:
                in_ol = True
                html_lines.append("<ol>")
            item_text = re.sub(r"^\d+\.\s+", "", stripped)
            html_lines.append(f"<li>{inline_format(item_text)}</li>")
            continue
        else:
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False

        # Empty lines
        if not stripped:
            continue

        # 8. Horizontal rules
        if re.match(r"^(\-{3,}|\*{3,}|_{3,})$", stripped):
            html_lines.append("<hr/>")
            continue

        # 9. Headings
        if stripped.startswith("# "):
            html_lines.append(f"<h1>{inline_format(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{inline_format(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{inline_format(stripped[4:])}</h3>")
        elif stripped.startswith("#### "):
            html_lines.append(f"<h4>{inline_format(stripped[5:])}</h4>")
        elif stripped.startswith("##### "):
            html_lines.append(f"<h5>{inline_format(stripped[6:])}</h5>")
        elif stripped.startswith("###### "):
            html_lines.append(f"<h6>{inline_format(stripped[7:])}</h6>")
        else:
            # Paragraph
            html_lines.append(f"<p>{inline_format(stripped)}</p>")

    # Close trailing open tags
    if in_ul: html_lines.append("</ul>")
    if in_ol: html_lines.append("</ol>")
    if in_table: html_lines.append("</tbody></table></div>")
    if in_blockquote: html_lines.append("</blockquote>")
    if in_callout: html_lines.append("</div>")

    return "\n".join(html_lines)

# ----------------------------------------------------------------------
# Headless Chromium Browser Discovery
# ----------------------------------------------------------------------

def find_chromium_browser() -> str:
    """Discovers available Chromium-based browser on Windows, macOS, or Linux."""
    candidates = []
    
    if sys.platform == "win32":
        candidates = [
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    else: # Linux / Unix
        for bin_name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"]:
            path = shutil.which(bin_name)
            if path:
                candidates.append(path)

    for path in candidates:
        if path and os.path.exists(path):
            return path
            
    return None

# ----------------------------------------------------------------------
# Converter Core
# ----------------------------------------------------------------------

def convert(
    input_file: str,
    output_file: str = None,
    theme: str = "default",
    custom_css: str = None,
    page_size: str = "A4",
    orientation: str = "portrait",
    margin: str = "16mm 14mm 16mm 14mm",
    header_footer: bool = False,
    browser_path: str = None,
    keep_html: bool = False
) -> str:
    """Converts a markdown file to PDF using headless Chromium."""
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {input_path}")
        
    if not output_file:
        output_path = input_path.with_suffix(".pdf")
    else:
        output_path = Path(output_file).resolve()

    # Browser discovery
    browser_exe = browser_path or find_chromium_browser()
    if not browser_exe or not os.path.exists(browser_exe):
        raise RuntimeError(
            "No compatible Chromium browser found (Microsoft Edge, Google Chrome, or Brave).\n"
            "Please install Microsoft Edge / Chrome or specify --browser-path."
        )

    # Read Markdown
    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Select / Compose CSS
    if custom_css and os.path.exists(custom_css):
        with open(custom_css, "r", encoding="utf-8") as f:
            css_rules = f.read()
    else:
        css_rules = THEMES.get(theme.lower(), DEFAULT_THEME)

    page_css = f"""
    @page {{
        size: {page_size} {orientation};
        margin: {margin};
    }}
    """

    html_body = parse_markdown(md_text)
    document_title = input_path.stem.replace("_", " ").replace("-", " ").title()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{document_title}</title>
<style>
{page_css}
{css_rules}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # Write temporary HTML
    temp_dir = tempfile.gettempdir()
    temp_html_path = Path(temp_dir) / f"{input_path.stem}_temp_print.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Convert to URL format
    html_url = temp_html_path.as_uri()

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={output_path}",
        html_url
    ]

    if not header_footer:
        cmd.insert(4, "--no-pdf-header-footer")

    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if not keep_html and temp_html_path.exists():
        temp_html_path.unlink()

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError("PDF rendering failed. Check permissions or input file structure.")

    return str(output_path)

# ----------------------------------------------------------------------
# CLI Interface
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="md2pdf",
        description="Zero-dependency Markdown to PDF converter using headless browser rendering."
    )
    parser.add_argument("input", help="Path to input Markdown (.md) file")
    parser.add_argument("-o", "--output", help="Path to output PDF file (default: same name as input)")
    parser.add_argument("-t", "--theme", choices=["default", "dark", "academic"], default="default", help="Built-in theme style (default: default)")
    parser.add_argument("-c", "--css", help="Path to custom CSS file for styling override")
    parser.add_argument("-s", "--page-size", default="A4", choices=["A4", "Letter", "Legal", "A3", "A5"], help="Page size (default: A4)")
    parser.add_argument("-r", "--orientation", default="portrait", choices=["portrait", "landscape"], help="Page orientation (default: portrait)")
    parser.add_argument("-m", "--margin", default="16mm 14mm 16mm 14mm", help="Page margins (default: '16mm 14mm 16mm 14mm')")
    parser.add_argument("--header-footer", action="store_true", help="Include browser header (date/title) and footer (URL/page)")
    parser.add_argument("--browser-path", help="Explicit path to Chrome/Edge binary executable")
    parser.add_argument("--keep-html", action="store_true", help="Keep intermediate HTML file after conversion")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    try:
        pdf_file = convert(
            input_file=args.input,
            output_file=args.output,
            theme=args.theme,
            custom_css=args.css,
            page_size=args.page_size,
            orientation=args.orientation,
            margin=args.margin,
            header_footer=args.header_footer,
            browser_path=args.browser_path,
            keep_html=args.keep_html
        )
        print(f"[OK] Successfully created: {pdf_file}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
