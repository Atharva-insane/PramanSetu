import os
import shutil
import json

BASE_DIR = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI"

# 1. Create directories
dirs_to_create = [
    "docs/00_START_HERE",
    "docs/01_PROBLEM_AND_SOLUTION",
    "docs/02_USER_DOCUMENTATION",
    "docs/03_DEMO_AND_PRESENTATION",
    "docs/04_TECHNICAL",
    "docs/05_FORENSIC_ENGINE",
    "docs/06_CITIZEN_AND_RTI",
    "docs/07_SECURITY",
    "docs/08_TESTING",
    "docs/09_DEPLOYMENT",
    "docs/10_HACKATHON_SUBMISSION",
    "docs/pdf",
    "docs/datasets",
    "docs/evidence/screenshots",
    "docs/archive",
    "submission"
]

for d in dirs_to_create:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

print("[INFO] Directories created successfully.")

# 2. Copy PDFs to docs/pdf/
pdf_files = [
    "PramanSetu_Complete_Demo_User_Judge_Guide.pdf",
    "PramanSetu_How_The_Application_Works.pdf",
    "PramanSetu_Exhaustive_Matrix_Test_Catalog.pdf",
    "CITIZEN_RTI_EXTREME_AUDIT.pdf",
    "CITIZEN_BROWSER_ACCEPTANCE_TEST.pdf"
]

for f in pdf_files:
    src = os.path.join(BASE_DIR, f)
    dst = os.path.join(BASE_DIR, "docs/pdf", f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[COPIED] {f} -> docs/pdf/{f}")

# 3. Copy datasets to docs/datasets/
dataset_files = [
    "MATRIX_TEST_CASES.csv",
    "MATRIX_TEST_CASES.json",
    "MATRIX_ACCURACY_AUDIT.json",
    "CITIZEN_TEST_CASES.csv",
    "CITIZEN_TEST_CASES.json"
]

for f in dataset_files:
    src = os.path.join(BASE_DIR, f)
    dst = os.path.join(BASE_DIR, "docs/datasets", f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[COPIED] {f} -> docs/datasets/{f}")

# 4. Copy primary markdown files into organized docs sections
file_mappings = [
    ("PramanSetu_Complete_Demo_User_Judge_Guide.md", "docs/02_USER_DOCUMENTATION/COMPLETE_USER_GUIDE.md"),
    ("PramanSetu_How_The_Application_Works.md", "docs/02_USER_DOCUMENTATION/HOW_THE_APPLICATION_WORKS.md"),
    ("PramanSetu_Complete_Demo_User_Judge_Guide.md", "docs/03_DEMO_AND_PRESENTATION/DEMO_MASTER_GUIDE.md"),
    ("MATRIX_ACCURACY_AUDIT.md", "docs/05_FORENSIC_ENGINE/MATRIX_ACCURACY_AUDIT.md"),
    ("PramanSetu_Exhaustive_Matrix_Test_Catalog.md", "docs/08_TESTING/MATRIX_TEST_CATALOG.md"),
    ("CITIZEN_RTI_EXTREME_AUDIT.md", "docs/06_CITIZEN_AND_RTI/CITIZEN_RTI_AUDIT.md"),
    ("CITIZEN_BROWSER_ACCEPTANCE_TEST.md", "docs/06_CITIZEN_AND_RTI/CITIZEN_BROWSER_ACCEPTANCE.md"),
    ("DEPLOYMENT_GUIDE.md", "docs/09_DEPLOYMENT/PRODUCTION_CAPABLE_DEPLOYMENT.md")
]

for src_name, dst_rel in file_mappings:
    src = os.path.join(BASE_DIR, src_name)
    dst = os.path.join(BASE_DIR, dst_rel)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[ORGANIZED] {src_name} -> {dst_rel}")

# 5. Move HTML intermediate print files to docs/archive/
html_intermediates = [
    "CITIZEN_BROWSER_ACCEPTANCE_TEST.html",
    "CITIZEN_RTI_EXTREME_AUDIT.html",
    "PramanSetu_Complete_Demo_User_Judge_Guide.html",
    "PramanSetu_Exhaustive_Matrix_Test_Catalog.html",
    "PramanSetu_How_The_Application_Works.html",
    "test_catalog_print.html"
]

for h in html_intermediates:
    src = os.path.join(BASE_DIR, h)
    dst = os.path.join(BASE_DIR, "docs/archive", h)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[ARCHIVED] {h} -> docs/archive/{h}")

print("[SUCCESS] Repository organization script finished initial pass.")
