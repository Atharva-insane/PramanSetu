import os
import subprocess
import re

BASE_DIR = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI"
MD_PATH = os.path.join(BASE_DIR, "CITIZEN_BROWSER_ACCEPTANCE_TEST.md")
HTML_PATH = os.path.join(BASE_DIR, "CITIZEN_BROWSER_ACCEPTANCE_TEST.html")
PDF_PATH = os.path.join(BASE_DIR, "CITIZEN_BROWSER_ACCEPTANCE_TEST.pdf")

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Build Rich, Professional HTML with Print CSS
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PramanSetu — Final Citizen Browser Acceptance Test Report</title>
<style>
    @page {
        size: A4 portrait;
        margin: 16mm 14mm 16mm 14mm;
        @top-center {
            content: "PramanSetu (प्रमाण सेतु) — Citizen Browser Acceptance Test Record";
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 7.5pt;
            color: #64748b;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3px;
            margin-bottom: 6mm;
        }
        @bottom-left {
            content: "Live Browser Acceptance Record | Real Citizen User Journey";
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 7.5pt;
            color: #94a3b8;
        }
        @bottom-right {
            content: "Page " counter(page);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 7.5pt;
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
        font-size: 8.5pt;
        line-height: 1.5;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    /* Cover Page */
    .cover-page {
        page-break-after: always;
        height: 100%;
        min-height: 245mm;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 25mm 15mm 20mm 15mm;
        border: 2px solid #0284c7;
        border-radius: 12px;
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%);
        margin-bottom: 10mm;
    }

    .cover-badge {
        display: inline-block;
        background-color: #0284c7;
        color: #ffffff;
        font-weight: 700;
        font-size: 8.5pt;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 20px;
        margin-bottom: 15px;
    }

    .cover-title {
        font-size: 23pt;
        font-weight: 800;
        color: #0c4a6e;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }

    .cover-subtitle {
        font-size: 13pt;
        font-weight: 600;
        color: #0369a1;
        margin: 0 0 14px 0;
    }

    .cover-desc {
        font-size: 10pt;
        color: #334155;
        max-width: 150mm;
        margin: 0 auto 25px auto;
        line-height: 1.45;
    }

    .cover-meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        width: 100%;
        max-width: 150mm;
        text-align: left;
        margin-bottom: 25px;
    }

    .meta-box {
        background: #ffffff;
        border: 1px solid #bae6fd;
        border-radius: 6px;
        padding: 8px 12px;
    }

    .meta-label {
        font-size: 7pt;
        text-transform: uppercase;
        font-weight: 700;
        color: #0369a1;
        margin-bottom: 2px;
    }

    .meta-value {
        font-size: 9pt;
        font-weight: 600;
        color: #0f172a;
    }

    .cover-footer {
        margin-top: auto;
        font-size: 8pt;
        color: #075985;
        border-top: 1px solid #e0f2fe;
        padding-top: 12px;
        width: 100%;
        max-width: 150mm;
    }

    /* Headings */
    h1 {
        font-size: 16pt;
        font-weight: 800;
        color: #0c4a6e;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }

    h2 {
        font-size: 12pt;
        font-weight: 700;
        color: #0369a1;
        margin-top: 14px;
        margin-bottom: 6px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 3px;
        page-break-after: avoid;
    }

    h3 {
        font-size: 10pt;
        font-weight: 600;
        color: #0284c7;
        margin-top: 10px;
        margin-bottom: 4px;
        page-break-after: avoid;
    }

    p, li {
        color: #334155;
        margin-top: 0;
        margin-bottom: 5px;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0 12px 0;
        font-size: 7.5pt;
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
        background: #0c4a6e;
        color: #ffffff;
        font-weight: 600;
        text-align: left;
        padding: 5px 6px;
        border: 1px solid #0369a1;
    }

    td {
        padding: 4px 6px;
        border: 1px solid #cbd5e1;
        vertical-align: top;
    }

    tr:nth-child(even) td {{
        background: #f8fafc;
    }}

    code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 7.5pt;
        background: #f1f5f9;
        padding: 1px 3px;
        border-radius: 3px;
        color: #0f172a;
        border: 1px solid #e2e8f0;
    }

    pre {
        background: #0c4a6e;
        color: #f8fafc;
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 7.5pt;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        overflow-x: auto;
        margin: 8px 0;
        page-break-inside: avoid;
    }

    pre code {
        background: transparent;
        border: none;
        color: #38bdf8;
        padding: 0;
    }

    hr {
        border: 0;
        height: 1px;
        background: #cbd5e1;
        margin: 12px 0;
    }
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
    <div class="cover-badge">Live Browser Acceptance Record</div>
    <div class="cover-title">PramanSetu (CivicAudit AI)</div>
    <div class="cover-subtitle">Final Citizen Browser Acceptance Test Report</div>
    <div class="cover-desc">
        Comprehensive real user journey acceptance record validating initial page intake, language switching, evidence upload, AI discrepancy translation, statutory RTI Form A generation, clipboard actions, and mobile responsiveness.
    </div>

    <div class="cover-meta-grid">
        <div class="meta-box">
            <div class="meta-label">Test Target</div>
            <div class="meta-value">http://localhost:3000/citizen</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Acceptance Decision</div>
            <div class="meta-value">A. ACCEPTED (Fully Validated)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Audited Scenario</div>
            <div class="meta-value">Village Community Drainage (Rampur)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Calculated Verdict</div>
            <div class="meta-value">FLAGGED (Risk Score 60/100)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Statutory Deadline</div>
            <div class="meta-value">22 September 2026 (30 Days)</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Persistence Audit</div>
            <div class="meta-value">Verified in SQLite (audit_id: RTI-202608-024CE6)</div>
        </div>
    </div>

    <div class="cover-footer">
        <strong>PramanSetu National Evidence Intelligence Gateway</strong><br>
        Published & Verified: August 2026 | Official Browser Acceptance Validation Record
    </div>
</div>

<!-- Main Body -->
<div class="main-content">
__BODY_CONTENT__
</div>

</body>
</html>
"""

def md_to_html(md):
    content = md
    content = re.sub(r"^# 🏛️ PramanSetu.*?(?=## 1\. Acceptance Objectives|\Z)", "", content, flags=re.DOTALL)

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
                if len(table_lines) >= 2:
                    t_html = ["<table>"]
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

    if in_table and len(table_lines) >= 2:
        t_html = ["<table>"]
        headers = [c.strip() for c in table_lines[0].split("|")[1:-1]]
        t_html.append("<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>")
        t_html.append("<tbody>")
        for row_line in table_lines[2:]:
            if "|" in row_line:
                cols = [c.strip() for c in row_line.split("|")[1:-1]]
                t_html.append("<tr>" + "".join(f"<td>{c}</td>" for c in cols) + "</tr>")
        t_html.append("</tbody></table>")
        new_lines.append("".join(t_html))

    content = "\n".join(new_lines)
    content = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", content, flags=re.MULTILINE)
    content = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", content, flags=re.MULTILINE)
    content = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", content, flags=re.MULTILINE)
    content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", content)
    content = re.sub(r"\*(.*?)\*", r"<em>\1</em>", content)
    content = re.sub(r"`(.*?)`", r"<code>\1</code>", content)
    content = re.sub(r"```(.*?)\n(.*?)```", r"<pre><code>\2</code></pre>", content, flags=re.DOTALL)
    return content

formatted_html = html_template.replace("__BODY_CONTENT__", md_to_html(md_content))

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(formatted_html)

print("[INFO] Generated print-ready HTML:", HTML_PATH)

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

edge_bin = None
for p in edge_paths:
    if os.path.exists(p):
        edge_bin = p
        break

if not edge_bin:
    print("[ERROR] Microsoft Edge executable not found.")
    sys.exit(1)

cmd = [
    edge_bin,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

print("[INFO] Rendering PDF via headless Edge...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(PDF_PATH):
    size_kb = os.path.getsize(PDF_PATH) / 1024.0
    print(f"[SUCCESS] Generated Acceptance PDF ({size_kb:.1f} KB) at: {PDF_PATH}")
else:
    print(f"[ERROR] Headless PDF generation failed. Code: {res.returncode}")
    print("Stderr:", res.stderr)
