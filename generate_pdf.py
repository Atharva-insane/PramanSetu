import os
import subprocess
import re

MD_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\PramanSetu_Complete_Demo_User_Judge_Guide.md"
HTML_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\PramanSetu_Complete_Demo_User_Judge_Guide.html"
PDF_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\PramanSetu_Complete_Demo_User_Judge_Guide.pdf"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Build Rich, Professional HTML with Print CSS
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PramanSetu (CivicAudit AI) — Complete User Manual, Demonstration Master Guide & Evaluator Handbook</title>
<style>
    @page {
        size: A4 portrait;
        margin: 18mm 15mm 18mm 15mm;
        @top-center {
            content: "PramanSetu (प्रमाण सेतु) — CivicAudit AI | Official Evaluation Handbook";
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 8pt;
            color: #64748b;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
            margin-bottom: 8mm;
        }
        @bottom-left {
            content: "Version 2.1.0 (Production-Hardened Single-Node Release)";
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

    /* Cover Page */
    .cover-page {
        page-break-after: always;
        height: 100%;
        min-height: 240mm;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30mm 15mm 20mm 15mm;
        border: 2px solid #0284c7;
        border-radius: 12px;
        background: linear-gradient(180deg, #f8fafc 0%, #f0f9ff 100%);
        margin-bottom: 10mm;
    }

    .cover-badge {
        display: inline-block;
        background-color: #0284c7;
        color: #ffffff;
        font-weight: 700;
        font-size: 9pt;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 20px;
        margin-bottom: 15px;
    }

    .cover-title {
        font-size: 26pt;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }

    .cover-subtitle {
        font-size: 14pt;
        font-weight: 600;
        color: #0369a1;
        margin: 0 0 16px 0;
    }

    .cover-desc {
        font-size: 11pt;
        color: #475569;
        max-width: 140mm;
        margin: 0 auto 30px auto;
        line-height: 1.5;
    }

    .cover-meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        width: 100%;
        max-width: 140mm;
        text-align: left;
        margin-bottom: 30px;
    }

    .meta-box {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px 14px;
    }

    .meta-label {
        font-size: 7.5pt;
        text-transform: uppercase;
        font-weight: 700;
        color: #64748b;
        margin-bottom: 2px;
    }

    .meta-value {
        font-size: 9.5pt;
        font-weight: 600;
        color: #0f172a;
    }

    .cover-footer {
        font-size: 8.5pt;
        color: #64748b;
        margin-top: auto;
    }

    /* Typography */
    h1 {
        font-size: 15pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 4px;
        margin-top: 24px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }

    h2 {
        font-size: 12pt;
        font-weight: 700;
        color: #0369a1;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 3px;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }

    h3 {
        font-size: 10.5pt;
        font-weight: 700;
        color: #334155;
        margin-top: 14px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }

    p, li {
        color: #334155;
        margin-top: 0;
        margin-bottom: 6px;
    }

    ul, ol {
        margin-top: 0;
        margin-bottom: 8px;
        padding-left: 20px;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 14px 0;
        font-size: 8.5pt;
        page-break-inside: auto;
    }

    tr {
        page-break-inside: avoid;
        page-break-after: auto;
    }

    thead {
        display: table-header-group;
    }

    th {
        background-color: #0f172a;
        color: #ffffff;
        font-weight: 600;
        text-align: left;
        padding: 6px 8px;
        border: 1px solid #334155;
    }

    td {
        padding: 5px 8px;
        border: 1px solid #cbd5e1;
        vertical-align: top;
    }

    tbody tr:nth-child(even) {
        background-color: #f8fafc;
    }

    /* Callouts & Alert Boxes */
    .callout {
        border-left: 4px solid #0284c7;
        background-color: #f0f9ff;
        padding: 8px 12px;
        margin: 10px 0;
        border-radius: 0 6px 6px 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }

    .callout-important {
        border-left-color: #e11d48;
        background-color: #fff1f2;
    }

    .callout-tip {
        border-left-color: #059669;
        background-color: #ecfdf5;
    }

    .callout-title {
        font-weight: 700;
        margin-bottom: 3px;
    }

    .callout-important .callout-title { color: #be123c; }
    .callout-tip .callout-title { color: #047857; }
    .callout .callout-title { color: #0369a1; }

    /* Code Blocks */
    pre {
        background-color: #0f172a;
        color: #f1f5f9;
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8pt;
        line-height: 1.4;
        overflow-x: auto;
        margin: 8px 0;
        page-break-inside: avoid;
        border: 1px solid #334155;
    }

    code {
        font-family: 'Consolas', 'Courier New', monospace;
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 8.5pt;
    }

    pre code {
        background-color: transparent;
        color: inherit;
        padding: 0;
    }

    /* Badges & Highlights */
    .badge {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 7.5pt;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-clear { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .badge-review { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .badge-flagged { background: #ffe4e6; color: #9f1239; border: 1px solid #fecdd3; }

    hr {
        border: none;
        border-top: 1px solid #cbd5e1;
        margin: 16px 0;
    }
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
    <div class="cover-badge">National Forensic Intelligence</div>
    <div class="cover-title">PramanSetu (प्रमाण सेतु)</div>
    <div class="cover-subtitle">CivicAudit AI — National Evidence Intelligence & Forensic Risk Gateway</div>
    <div class="cover-desc">
        Complete User Manual, Interactive Demonstration Master Guide & Official Evaluator Handbook.<br>
        Standard Operating Procedures, Forensic Engine Specifications, and Competition Showcase.
    </div>

    <div class="cover-meta-grid">
        <div class="meta-box">
            <div class="meta-label">Legislative Mandate</div>
            <div class="meta-value">GFR 2017 Rule 175 & RTI Act § 6(1)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Current Release</div>
            <div class="meta-value">Version 2.1.0 (Hardened Single-Node)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Automated Test Verification</div>
            <div class="meta-value">41 / 41 Tests Passing (100% Pass Rate)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Architecture Stack</div>
            <div class="meta-value">FastAPI 0.115 + Next.js 16.3 + SQLite</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Localization Support</div>
            <div class="meta-value">Tri-lingual (English, हिंदी, தமிழ்)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Security & Access Control</div>
            <div class="meta-value">HS256 Bearer JWT + PBKDF2 + RBAC</div>
        </div>
    </div>

    <div class="cover-footer">
        <strong>Government Technology Demonstration Package</strong><br>
        Published & Verified: August 2026 | Developed for State Infrastructure Vigilance Directorates
    </div>
</div>

<!-- Main Body -->
<div class="main-content">
__BODY_CONTENT__
</div>

</body>
</html>
"""

# Simple Markdown to HTML converter for formatted printing
def md_to_html(md):
    content = md
    
    # Strip metadata header block from MD since cover page handles it
    content = re.sub(r"^# 🏛️ PramanSetu.*?(?=# 1\. Cover Page|\Z)", "", content, flags=re.DOTALL)
    
    # Convert block alerts > [!IMPORTANT] and > [!TIP]
    def replace_callout(match):
        ctype = match.group(1).lower()
        body = match.group(2).strip()
        css_class = "callout"
        title = "NOTE"
        if ctype == "important":
            css_class = "callout callout-important"
            title = "CRITICAL INSTITUTIONAL BOUNDARY"
        elif ctype == "tip":
            css_class = "callout callout-tip"
            title = "EVALUATOR & DEMO TIP"
        return f'<div class="{css_class}"><div class="callout-title">{title}</div><p>{body}</p></div>'

    content = re.sub(r">\s*\[!(IMPORTANT|TIP|NOTE)\]\s*\n((?:>.*\n?)+)", lambda m: replace_callout(m), content)
    content = re.sub(r"^>\s*(.*)$", r"\1", content, flags=re.MULTILINE)

    # Convert Tables
    lines = content.split("\n")
    in_table = False
    table_lines = []
    new_lines = []
    
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

    return content

formatted_html = html_template.replace("__BODY_CONTENT__", md_to_html(md_content))

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(formatted_html)

print("HTML TEMPLATE WRITTEN:", HTML_PATH)

# Execute Headless Edge/Chrome to generate PDF
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

print("RUNNING HEADLESS PDF CONVERSION...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("PDF GENERATION COMPLETED. CODE:", res.returncode)
if os.path.exists(PDF_PATH):
    print("SUCCESS: PDF CREATED AT:", PDF_PATH)
    print("PDF SIZE:", os.path.getsize(PDF_PATH), "bytes")
else:
    print("ERROR: PDF was not created!")
