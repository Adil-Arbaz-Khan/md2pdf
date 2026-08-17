# md2pdf 📄✨

> **Zero-dependency, high-fidelity Markdown to PDF converter powered by your system's built-in Chromium / Edge engine.**

Convert Markdown documents into publication-ready, beautifully styled PDFs with syntax highlighting, clean typography, tables, and GitHub-style callouts — without installing massive LaTeX toolchains, Pandoc, Node.js, or heavyweight Python dependencies.

---

## ⚡ Highlights

- **Zero External Dependencies:** Built entirely with the Python Standard Library. No `pip install` required.
- **Native Browser Rendering Engine:** Leverages the headless Microsoft Edge, Google Chrome, or Brave browser already on your machine for pixel-perfect CSS3 rendering.
- **Built-in Themes:** Comes with `default` (modern clean), `dark` (developer dark mode), and `academic` (formal serif paper) styles.
- **GitHub Alert Callouts:** Full support for `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, and `> [!CAUTION]`.
- **Advanced Markdown Support:** Tables, code blocks, checklists (`- [x]`), images, blockquotes, and explicit page breaks.
- **Cross-Platform:** Works seamlessly across Windows, macOS, and Linux.

---

## 🚀 Quick Start

### 1. Requirements
* **Python 3.8+**
* Any Chromium-based browser (*Microsoft Edge, Google Chrome, Brave, or Chromium*).

### 2. Basic Usage

Convert any Markdown file to PDF with a single command:

```bash
python md2pdf.py document.md
```
*(This automatically creates `document.pdf` in the same directory).*

---

## 📖 Command Line Options

```text
usage: md2pdf [-h] [-o OUTPUT] [-t {default,dark,academic}] [-c CSS]
              [-s {A4,Letter,Legal,A3,A5}] [-r {portrait,landscape}]
              [-m MARGIN] [--header-footer] [--browser-path BROWSER_PATH]
              [--keep-html] [-v]
              input

Zero-dependency Markdown to PDF converter using headless browser rendering.

positional arguments:
  input                 Path to input Markdown (.md) file

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Path to output PDF file (default: same name as input)
  -t, --theme {default,dark,academic}
                        Built-in theme style (default: default)
  -c, --css CSS         Path to custom CSS file for styling override
  -s, --page-size {A4,Letter,Legal,A3,A5}
                        Page size (default: A4)
  -r, --orientation {portrait,landscape}
                        Page orientation (default: portrait)
  -m, --margin MARGIN   Page margins (default: '16mm 14mm 16mm 14mm')
  --header-footer       Include browser header (date/title) and footer (URL/page)
  --browser-path BROWSER_PATH
                        Explicit path to Chrome/Edge binary executable
  --keep-html           Keep intermediate HTML file after conversion
  -v, --version         show program's version number and exit
```

---

## 💡 Examples

### 1. Export with Dark Mode Theme
```bash
python md2pdf.py notes.md -t dark -o notes_dark.pdf
```

### 2. Export as Landscape US Letter Document
```bash
python md2pdf.py presentation.md -s Letter -r landscape
```

### 3. Apply Custom CSS Stylesheet
```bash
python md2pdf.py report.md -c my_branding.css -o final_report.pdf
```

### 4. Explicit Page Breaks
Insert a manual page break anywhere in your Markdown:
```markdown
# Section One
Content for page one...

\pagebreak

# Section Two
Content starting at the top of page two...
```

---

## 🎨 Themes

| Theme | Description | Ideal For |
| :--- | :--- | :--- |
| **`default`** | Modern sans-serif (Plus Jakarta Sans), dark code blocks, slate borders | Technical docs, cheatsheets, notes |
| **`dark`** | Deep slate background, high-contrast text, glowing cyan code blocks | Developer manuals, terminal logs |
| **`academic`** | Classic serif typography (Times New Roman), justified margins, formal tables | Research papers, formal essays |

---

## 🛠️ Architecture & Under the Hood

```
┌──────────────┐     md2pdf Parser Engine          ┌────────────────┐     Headless Chromium Engine     ┌──────────────┐
│ Markdown Doc │ ────────────────────────────────> │ Clean HTML5    │ ───────────────────────────────> │ Rendered PDF │
│   (.md)      │   (Generates DOM + Theme CSS)     │ + @page Styles │     (msedge / chrome headless) │   (.pdf)     │
└──────────────┘                                   └────────────────┘                                  └──────────────┘
```

1. **Parser:** Parses Markdown structures (headers, code snippets, lists, tables, callouts) into semantic HTML5.
2. **Styler:** Injects tailored CSS3 with print media directives (`@page`, `page-break-inside: avoid`).
3. **Renderer:** Launches Chromium in headless mode to rasterize the DOM and compile the vector PDF via `--print-to-pdf`.

---

## 📦 Python Module Usage

You can also import `md2pdf` directly inside your Python scripts:

```python
from md2pdf import convert

# Simple conversion
pdf_path = convert("README.md")

# Advanced conversion with options
pdf_path = convert(
    input_file="report.md",
    output_file="dist/report.pdf",
    theme="academic",
    page_size="Letter",
    margin="20mm 15mm 20mm 15mm"
)
print(f"Generated PDF: {pdf_path}")
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
