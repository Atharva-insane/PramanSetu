# 🏛️ PramanSetu (प्रमाण सेतु) — CivicAudit AI

> **National Evidence Intelligence, Multi-Vector Forensic Risk Gateway & Grassroots Citizen Social Audit Subsystem**

[![Python Version](https://img.shields.io/badge/Python-3.14-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15.0+-black.svg)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19.0+-61DAFB.svg)](https://react.dev)
[![Tests Passing](https://img.shields.io/badge/Tests-231%2F231%20Passed-success.svg)](docs/08_TESTING/TESTING_OVERVIEW.md)
[![Compliance](https://img.shields.io/badge/Compliance-GFR%20Rule%20175%20%7C%20RTI%20Act%202005-orange.svg)](docs/01_PROBLEM_AND_SOLUTION/PROBLEM_STATEMENT_ALIGNMENT.md)

---

## 🏆 Problem Statement 3: AI for Civic & Legal Empowerment
**Theme**: *Civic Tech, Legal Access and Government Transparency*  
**Challenge**: *Build an AI system that helps a citizen understand and act on their civic or legal rights, translating bureaucratic complexity into a clear, guided path.*

---

## 🎯 The Core Problem

In public infrastructure projects across developing economies, billions of rupees are disbursed annually against fraudulent progress claims. Unscrupulous contractors recycle photographs from previous projects, bill for "ghost workers" using invalid Aadhaar numbers, and claim 100% finished asphalt over unpaved mud tracks. 

At the same time, rural citizens and Gram Panchayat members observing these incomplete works face massive legal and bureaucratic barriers when attempting to demand official records under the **Right to Information (RTI) Act 2005** or file public grievance petitions.

---

## 💡 Our Solution: PramanSetu

**PramanSetu (प्रमाण सेतु)** is a dual-sided civic integrity platform that bridges grassroots citizen vigilance with institutional procurement accountability:

1. **Institutional Vigilance Cockpit (`/audit`, `/demo`, `/analytics`)**: Automatically evaluates public works disbursement claims across **10 physical and mathematical forensic vectors** to detect asset recycling, geographic offsets, satellite vegetation anomalies, and statutory wage ceiling violations under **General Financial Rules (GFR 2017) Rule 175**.
2. **Grassroots Citizen Social Audit Gateway (`/citizen`)**: Enables citizens to upload on-site smartphone photos, translates technical forensic discrepancies into plain-language findings, and auto-generates statutory **Section 6(1) Form 'A' RTI petitions** and **CPGRAMS grievance petitions** with an automated 30-day statutory appeal countdown tracker.

---

## 🌟 Why PramanSetu Is Different

- **10 Independent Physical Forensic Vectors**: Evaluates spatial, temporal, visual, and mathematical telemetry rather than relying on unverified text claims.
- **Multilingual Grassroots Accessibility**: Fully operational in **English**, **Hindi (*हिन्दी*)**, and **Tamil (*தமிழ்*)**.
- **Automated RTI Form 'A' Legal Drafting**: Demands the 4 statutory engineering records (Measurement Books, labor muster rolls, quality test certificates, and disbursement vouchers).
- **Cryptographic Chain-of-Custody**: Issues tamper-evident **SHA-256 digital seals** verifiable via public QR codes (`/verify/[id]`).
- **Whistleblower Privacy**: Protects citizen anonymity by never storing personal identity records in the public database.

---

## 🔬 Core Feature Matrix

| Feature Area | User Capability | Statutory / Technical Alignment | Route |
|---|---|---|---|
| **Citizen Social Audit** | Upload worksite photo, receive plain-language discrepancy translation, and auto-generate Form A RTI | RTI Act 2005 Section 6(1) & CPGRAMS | [`/citizen`](http://localhost:3000/citizen) |
| **Statutory 30-Day Tracker** | Live countdown and date calculation for filing First Appeal under Section 19(1) | RTI Act Section 7(1) & 19(1) | [`/citizen`](http://localhost:3000/citizen) |
| **Institutional Forensic Intake** | Multi-vector photographic, spatial, and muster roll evaluation with instant risk score | GFR 2017 Rule 175 Procurement Standards | [`/audit`](http://localhost:3000/audit) |
| **Interactive Benchmark Demo** | One-click simulation of authentic rural roads vs high-risk fraud procurement schemes | Automated synthetic baseline testing | [`/demo`](http://localhost:3000/demo) |
| **Macro Vigilance Cockpit** | State-level dynamic KPI dashboard, contractor trust ratings, and GIS fraud maps | CVO Administrative Oversight | [`/analytics`](http://localhost:3000/analytics) |
| **Public QR Dossier Ledger** | Public cryptographic verification of administrative payment hold orders | Deterministic SHA-256 verification seal | [`/verify/[id]`](http://localhost:3000/verify/DOSSIER-202608-VAR001) |

---

## 🏗️ System Architecture

```text
+-----------------------------------------------------------------------------------+
|                        PRAMANSETU SYSTEM ARCHITECTURE                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ FRONTEND LAYER ]  Next.js 15 App Router | React 19 | Tailwind CSS | i18n       |
|                      Routes: / | /audit | /demo | /analytics | /citizen | /verify |
|                                                                                   |
|  [ GATEWAY LAYER ]   FastAPI 0.115+ | Sliding-Window Rate Limiter | Magic Bytes   |
|                                                                                   |
|  [ FORENSIC ENGINES] 1. 64-Bit DCT Perceptual Hashing (pHash)                     |
|                      2. Web Stock Asset Perceptual Search                         |
|                      3. WGS-84 Vincenty Ellipsoidal Geodesics                     |
|                      4. Copernicus Sentinel-2 Satellite Ground-Truth Anomaly      |
|                      5. Verhoeff D5 Dihedral Aadhaar & Wage Ceiling Math          |
|                      6. NOAA Solar Position Algorithm (SPA) & Weather             |
|                      7. Milestone & Surface Material Alignment                    |
|                      8. Gemini 2.0 Flash Multimodal Vision Forensics              |
|                      9. Laplacian Kernel Frequency Variance & Payload Bounds      |
|                      10. Calibrated Composite Risk Scoring (0-100 Clamped)        |
|                                                                                   |
|  [ LEGAL DRAFTING ]  Section 6(1) Form A RTI Application | CPGRAMS Grievance     |
|                                                                                   |
|  [ STORAGE & LEDGER] SQLite 3 (WAL Mode) | SHA-256 Cryptographic Verification     |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## ⚡ Quickstart & Local Execution

### 1. Prerequisites
- Python 3.10+ (Python 3.14 recommended)
- Node.js 18+ & npm
- Git

### 2. Start Backend Daemon (Port 8002)
```bash
# From workspace root
python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload
```

### 3. Start Frontend Web Server (Port 3000)
```bash
# In a separate terminal
cd frontend
npm install
npm run dev -- -p 3000
```
Open **`http://localhost:3000`** in your browser.

---

## 🧪 Automated Testing & Verification

Execute the complete **231-test automated test suite**:
```bash
py -3.14 -c "
import sys
sys.path.insert(0, r'C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\Lib\site-packages')
sys.path.insert(0, r'C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI')
sys.path.insert(0, r'C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\backend')
import pytest
sys.exit(pytest.main(['backend/tests/', '-v']))
"
```
- **Total Test Cases**: **231 Items (100% Passed)**
- **Combinatorial States Verified**: **1,024 / 1,024 Binary Scoring States**
- **Citizen Acceptance Tests**: **13 / 13 Passed in Live Browser**

---

## 📚 Master Documentation Index

- [**00_START_HERE / Project Overview**](docs/00_START_HERE/PROJECT_OVERVIEW.md) — 5-minute executive brief
- [**01_PROBLEM_AND_SOLUTION / Alignment**](docs/01_PROBLEM_AND_SOLUTION/PROBLEM_STATEMENT_ALIGNMENT.md) — Problem Statement 3 mapping
- [**02_USER_DOCUMENTATION / User Guide**](docs/02_USER_DOCUMENTATION/COMPLETE_USER_GUIDE.md) — Full platform user manual
- [**03_DEMO_AND_PRESENTATION / 10-Min Script**](docs/03_DEMO_AND_PRESENTATION/10_MINUTE_DEMO_SCRIPT.md) — Official video storyboard
- [**04_TECHNICAL / Architecture**](docs/04_TECHNICAL/ARCHITECTURE.md) — Technical architecture & data flow
- [**05_FORENSIC_ENGINE / Matrix Audit**](docs/05_FORENSIC_ENGINE/MATRIX_ACCURACY_AUDIT.md) — 28-section forensic matrix audit
- [**06_CITIZEN_AND_RTI / Citizen Audit**](docs/06_CITIZEN_AND_RTI/CITIZEN_RTI_AUDIT.md) — Citizen & RTI validation record
- [**07_SECURITY / Security Architecture**](docs/07_SECURITY/SECURITY_OVERVIEW.md) — Security & cryptography overview
- [**08_TESTING / Matrix Test Catalog**](docs/08_TESTING/MATRIX_TEST_CATALOG.md) — Complete 200+ test case catalog
- [**09_DEPLOYMENT / Production Deployment**](docs/09_DEPLOYMENT/PRODUCTION_CAPABLE_DEPLOYMENT.md) — Production operations manual
- [**10_HACKATHON_SUBMISSION / Submission Guide**](docs/10_HACKATHON_SUBMISSION/HACKATHON_SUBMISSION_GUIDE.md) — Final hackathon submission brief
- [**Master PDF Documentation**](docs/pdf/) — 5 Publication-quality PDF reports

---

## 🔗 Submission Prototype & Demo Links

- **Local Prototype URL**: `http://localhost:3000`
- **Citizen Portal**: `http://localhost:3000/citizen`
- **Benchmark Demo**: `http://localhost:3000/demo`
- **Macro Cockpit**: `http://localhost:3000/analytics`
- **Backend API**: `http://127.0.0.1:8002`
- **Hosted Prototype**: `[HOSTED_URL_OR_LOCAL_DEMO]`
- **Demo Video (<=10 Mins)**: `[DEMO_VIDEO_URL_TO_BE_ATTACHED]`

---

## ⚖️ Technical Boundaries & Known Assumptions

1. **RTI Legal Drafting**: Generates legally structured Section 6(1) Form 'A' application drafts; manual filing by the citizen with the Public Information Officer is required.
2. **Software PKI**: Implements HMAC-SHA256 asymmetric cryptographic seals; production deployment supports PKCS#11 hardware HSMs.
3. **Reference Data**: Evaluates against curated GIS anomaly polygons and local reference databases.
4. **AI Vision Fallback**: Seamlessly switches to offline Shannon Texture Entropy if Google Gemini API key is unconfigured.
