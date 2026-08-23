# CivicAudit AI — Enterprise Government Deployment Guide & Architecture Whitepaper

## 1. Executive Overview & Regulatory Mandate

**CivicAudit AI** is an AI-assisted pre-approval evidence intelligence gateway engineered for state infrastructure departments, municipal corporations, and vigilance directorates.

### Statutory Compliance
- **General Financial Rules (GFR 2017) Rule 175**: Directs Drawing & Disbursing Officers (DDO) to withhold fund disbursement upon evidence of material discrepancy, contractor ghost billing, or past asset recycling.
- **Section 6(1) Right to Information (RTI) Act, 2005**: Automates Section 6(1) Form A petitions and 30-day statutory response timelines for citizens and Gram Panchayats.
- **Section 65B Indian Evidence Act**: Embeds cryptographic SHA-256 seals, server IP logs, and chain-of-custody metadata into every electronic evidence dossier for court admissibility.

---

## 2. System Architecture

```
                                  [ Citizen & DDO Clients ]
                                             │
                                             ▼
                               [ Next.js 14 GovTech Portal ]
                                  (Port 3000 • SSR & Client)
                                             │
                                             ▼
                             [ FastAPI Multi-Vector Gateway ]
                                (Port 8002 • Uvicorn Async)
                                             │
                     ┌───────────────────────┼───────────────────────┐
                     ▼                       ▼                       ▼
           [ 10 Forensic Engines ]    [ SQLite/Postgres DB ]    [ Gemini 2.0 Vision ]
             • pHash 64-bit DCT         • Audit Ledger           • Multimodal Zero-Shot
             • Spatial EXIF GPS         • Contractor Profiles    • Visual Material Verifier
             • OpenCV Face Telemetry    • QR Verify Records
             • Ghost Labor Wage Calc
             • Solar Chrono-Forensics
```

---

## 3. Quickstart Deployment Options

### Option A: 1-Click Docker Deployment (Recommended for Production)

Prerequisites: [Docker](https://www.docker.com/) and Docker Compose installed.

```bash
# Clone and enter the repository
cd "CivicAudit AI"

# Build and launch both containers in detached mode
docker compose up -d --build
```

Access services:
* 🌐 **GovTech Frontend**: `http://localhost:3000`
* ⚡ **FastAPI Backend Gateway**: `http://localhost:8002/docs`

To stop:
```bash
docker compose down
```

---

### Option B: 1-Click Native Script Deployment

#### On Windows (PowerShell):
```powershell
.\start_production.ps1
```

#### On Linux / macOS:
```bash
chmod +x start_production.sh
./start_production.sh
```

---

## 4. Environment Configuration

Create a `.env` file in the root or set variables in your cloud deployment platform:

```env
# Optional Gemini API Key for Enhanced Multimodal Vision
GEMINI_API_KEY=your_gemini_api_key_here

# Backend Host & Port
HOST=127.0.0.1
PORT=8002

# Frontend Target Gateway URL
NEXT_PUBLIC_API_URL=http://127.0.0.1:8002
```

---

## 5. Security & Data Isolation (MeitY Guidelines)

1. **Air-Gapped & Offline Compatibility**:
   - The entire 10-vector forensic pipeline (pHash, spatial GPS, OpenCV, muster roll wage calculator, solar chrono-forensics) executes **100% locally on-premise** without sending sensitive tender records or contractor data to third-party servers.
   - If a Gemini API key is not configured, the system automatically uses local heuristics with zero downtime.

2. **Tamper-Evident SHA-256 Non-Repudiation**:
   - Every generated investigation dossier is sealed with a canonical SHA-256 hash.
   - Any modification to photographic pixels, tender IDs, or amounts invalidates the verification hash on `/verify`.

3. **Persistent SQLite / PostgreSQL Storage**:
   - SQLite is used by default with zero configuration required (`backend/data/civicaudit.db`).
   - For enterprise multi-region clusters, simply update `DATABASE_URL` in `config.py` to point to a PostgreSQL cluster.

---

## 6. Core API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/audit/milestone-claim` | Comprehensive 10-vector pre-approval forensic audit |
| `POST` | `/api/citizen/report` | Citizen social audit & Section 6(1) Form A RTI generator |
| `GET` | `/api/verify/{dossier_id}` | Public cryptographic QR verification endpoint |
| `GET` | `/api/analytics/geo-heatmap` | Regional project coordinates and risk ratings |
| `GET` | `/api/analytics/collusion-network` | Contractor collusion node-link syndicate graph |
| `GET` | `/api/analytics/temporal-trends` | Monthly disbursement vs intercepted funds |
| `GET` | `/api/contractors` | Contractor integrity trust scorecards & ratings |
| `GET` | `/api/health` | Gateway healthcheck and diagnostics |
