import os
import subprocess
import re

MD_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\PramanSetu_How_The_Application_Works.md"
HTML_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\PramanSetu_How_The_Application_Works.html"
PDF_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\PramanSetu_How_The_Application_Works.pdf"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Build Rich, Professional HTML with Print CSS
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PramanSetu (CivicAudit AI) — Complete Simple-Language Application Working Guide</title>
<style>
    @page {
        size: A4 portrait;
        margin: 18mm 15mm 18mm 15mm;
        @top-center {
            content: "PramanSetu (प्रमाण सेतु) — How the Application Works | Complete Working Guide";
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 8pt;
            color: #64748b;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
            margin-bottom: 8mm;
        }
        @bottom-left {
            content: "PramanSetu v2.1.0 (Production-Hardened Single-Node Release)";
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 8pt;
            color: #94a3b8;
        }
        @bottom-right {
            content: "Page " counter(page);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 8pt;
            font-weight: 600;
            color: #475569;
        }
    }

    @page:first {
        @top-center { content: normal; }
        @bottom-left { content: normal; }
        @bottom-right { content: normal; }
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 9.5pt;
        line-height: 1.55;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    .cover-page {
        page-break-after: always;
        height: 100%;
        min-height: 250mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 20mm 10mm 15mm 10mm;
        border: 2px solid #0284c7;
        border-radius: 4px;
        background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 40%, #ffffff 100%);
    }

    .cover-header {
        text-align: center;
    }

    .emblem-pill {
        display: inline-block;
        padding: 4px 16px;
        background: #0284c7;
        color: #ffffff;
        font-size: 8.5pt;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border-radius: 20px;
        margin-bottom: 12px;
    }

    .cover-title {
        font-size: 26pt;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }

    .cover-subtitle {
        font-size: 13pt;
        font-weight: 600;
        color: #0369a1;
        margin: 0 0 16px 0;
    }

    .cover-desc {
        font-size: 10pt;
        color: #475569;
        max-width: 140mm;
        margin: 0 auto 20px auto;
        line-height: 1.5;
    }

    .meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 20px 0;
    }

    .meta-card {
        padding: 10px 12px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .meta-card-label {
        font-size: 7.5pt;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
        margin-bottom: 3px;
    }

    .meta-card-val {
        font-size: 9pt;
        font-weight: 700;
        color: #0f172a;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }

    .cover-footer {
        text-align: center;
        border-top: 1px solid #e2e8f0;
        padding-top: 12px;
        font-size: 8pt;
        color: #64748b;
    }

    h1 {
        font-size: 15pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 4px;
        margin-top: 22pt;
        margin-bottom: 10pt;
        page-break-after: avoid;
    }

    h2 {
        font-size: 12pt;
        font-weight: 700;
        color: #0369a1;
        margin-top: 16pt;
        margin-bottom: 6pt;
        page-break-after: avoid;
    }

    h3 {
        font-size: 10pt;
        font-weight: 700;
        color: #334155;
        margin-top: 12pt;
        margin-bottom: 4pt;
        page-break-after: avoid;
    }

    p {
        margin-top: 0;
        margin-bottom: 8pt;
        text-align: justify;
    }

    ul, ol {
        margin-top: 0;
        margin-bottom: 8pt;
        padding-left: 18px;
    }

    li {
        margin-bottom: 3pt;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10pt 0 14pt 0;
        font-size: 8pt;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 5px 7px;
        text-align: left;
        vertical-align: top;
    }

    th {
        background-color: #f1f5f9;
        font-weight: 700;
        color: #0f172a;
    }

    tr:nth-child(even) {
        background-color: #f8fafc;
    }

    code {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
        background-color: #f1f5f9;
        padding: 1px 4px;
        border-radius: 3px;
        color: #0f172a;
        border: 1px solid #e2e8f0;
    }

    pre {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 8pt;
        line-height: 1.4;
        overflow-x: auto;
        margin: 8pt 0 12pt 0;
        page-break-inside: avoid;
    }

    pre code {
        background: transparent;
        border: none;
        color: #f8fafc;
        padding: 0;
    }

    blockquote {
        margin: 8pt 0 10pt 0;
        padding: 8px 12px;
        background-color: #f0f9ff;
        border-left: 3px solid #0284c7;
        color: #0369a1;
        font-size: 9pt;
        border-radius: 0 4px 4px 0;
        page-break-inside: avoid;
    }

    .badge {
        display: inline-block;
        padding: 1px 5px;
        font-size: 7.5pt;
        font-weight: 700;
        border-radius: 3px;
    }

    .badge-clear { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .badge-review { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .badge-flagged { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }

</style>
</head>
<body>

<div class="cover-page">
    <div class="cover-header">
        <div class="emblem-pill">CIVICAUDIT AI • SIMPLE-LANGUAGE WORKING GUIDE</div>
        <div class="cover-title">PramanSetu (प्रमाण सेतु)</div>
        <div class="cover-subtitle">How the Whole Application Actually Works</div>
        <div class="cover-desc">
            A complete, simple-language guide explaining every page, feature, forensic algorithm, scoring calculation, database record, and security control—written as if a senior developer friend is explaining it step-by-step.
        </div>
        
        <div class="meta-grid">
            <div class="meta-card">
                <div class="meta-card-label">Statutory Mandate</div>
                <div class="meta-card-val">GFR 2017 Rule 175 & Section 6(1) RTI Act</div>
            </div>
            <div class="meta-card">
                <div class="meta-card-label">Software Version</div>
                <div class="meta-card-val">v2.1.0 (Production-Hardened Single-Node)</div>
            </div>
            <div class="meta-card">
                <div class="meta-card-label">Automated Verification</div>
                <div class="meta-card-val">41 / 41 Passing Tests (100% Pass Rate)</div>
            </div>
            <div class="meta-card">
                <div class="meta-card-label">Technology Architecture</div>
                <div class="meta-card-val">FastAPI 0.115 + Next.js 16.3 + SQLite 3</div>
            </div>
        </div>
    </div>

    <div class="cover-footer">
        <strong>PramanSetu National Forensic Intelligence Gateway</strong><br>
        Published: August 2026 | Technical Handover & System Architecture Walkthrough
    </div>
</div>

<div class="content-body">
__BODY_CONTENT__
</div>

</body>
</html>
"""

def md_to_html(md_text):
    # Strip main title since it's in the cover page
    lines = md_text.split("\n")
    processed_lines = []
    skip_header = True
    
    for l in lines:
        if l.startswith("# 1. The Big Picture"):
            skip_header = False
        if not skip_header:
            processed_lines.append(l)
            
    content = "\n".join(processed_lines)

    # Convert Tables
    lines = content.split("\n")
    new_lines = []
    in_table = False
    table_lines = []
    
    for line in lines:
        if "|" in line and "-+-" not in line:
            in_table = True
            table_lines.append(line)
        else:
            if in_table:
                # Process table
                if len(table_lines) >= 2:
                    t_html = ["<table>"]
                    # Header
                    headers = [c.strip() for c in table_lines[0].split("|")[1:-1]]
                    t_html.append("<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>")
                    t_html.append("<tbody>")
                    for row_line in table_lines[2:]:
                        if "|" in row_line:
                            cols = [c.strip() for c in row_line.split("|")[1:-1]]
                            t_html.append("<tr>" + "".join(f"<td>{c}</td>" for c in cols) + "</tr>")
                    t_html.append("</tbody></table>")
                    new_lines.append("".join(t_html))
                in_table = False
                table_lines = []
            new_lines.append(line)

    content = "\n".join(new_lines)

    # Convert Headings
    content = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", content, flags=re.MULTILINE)
    content = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", content, flags=re.MULTILINE)
    content = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", content, flags=re.MULTILINE)

    # Convert Bold and Code
    content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", content)
    content = re.sub(r"\*(.*?)\*", r"<em>\1</em>", content)
    content = re.sub(r"`(.*?)`", r"<code>\1</code>", content)

    # Convert code blocks
    content = re.sub(r"```(.*?)\n(.*?)```", r"<pre><code>\2</code></pre>", content, flags=re.DOTALL)

    # Convert blockquotes
    content = re.sub(r"^> (.*?)$", r"<blockquote>\1</blockquote>", content, flags=re.MULTILINE)

    return content

formatted_html = html_template.replace("__BODY_CONTENT__", md_to_html(md_content))

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(formatted_html)

print("HTML WRITTEN:", HTML_PATH)

# Run Headless Browser PDF Conversion
browser = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(browser):
    browser = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    browser,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

print("RUNNING HEADLESS PDF GENERATION...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("PDF GENERATION COMPLETED. CODE:", res.returncode)
if os.path.exists(PDF_PATH):
    print("SUCCESS: PDF CREATED AT:", PDF_PATH)
    print("PDF SIZE:", os.path.getsize(PDF_PATH), "bytes")
else:
    print("ERROR: PDF was not created!")
