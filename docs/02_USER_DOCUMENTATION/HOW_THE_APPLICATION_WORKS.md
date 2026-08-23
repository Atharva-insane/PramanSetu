# PramanSetu (CivicAudit AI)
## How the Whole Application Actually Works
### A Complete Simple-Language Guide to Every Page, Feature, and Process

> *"From clicking a button to the database record: everything explained as if a senior developer friend is walking you through the entire system."*

---

# 1. The Big Picture: What is PramanSetu?

Let’s start with an honest question: **Why does PramanSetu exist in the first place?**

Every year, state governments and municipal corporations spend thousands of crores on public infrastructure: rural paved roads (PMGSY), drinking water pipelines (Jal Jeevan Mission), school classrooms, and stormwater drainage systems.

Historically, the process for paying contractors goes like this:
1. The contractor finishes a milestone (say, laying 5 km of asphalt road).
2. The contractor submits paper bills, measurement books, and a few printed photos.
3. The department disburses public funds from the state treasury via the **Public Financial Management System (PFMS)**.
4. Months or years later, government auditors review paper files. If the work was fake, substandard, or never done, the money has already left the treasury and is almost impossible to recover.

### Why Photographs and Metadata Aren't Automatically Trustworthy
In the age of smartphones, contractors submit digital photos as proof of work. But a digital photo is shockingly easy to manipulate:
* **Asset Recycling:** A contractor submits a photo taken during a *2023 pipeline project* to claim money for a *2024 road project*. To a tired desk officer, both look like dirt and gravel.
* **Geographic Displacements:** A contractor claims they built a culvert in Varanasi, but took a photo of a culvert in New Delhi (580 km away).
* **Stock Photo Theft:** A contractor downloads a high-resolution photo of a modern highway from Shutterstock or an online news article.
* **Ghost Labor Muster Rolls:** A claim lists 31 laborers with fabricated 12-digit Aadhaar numbers and inflated wage sums, but on-site photos show an empty field.
* **Material Mismatches:** The bill claims "100% Bituminous Asphalt Road Completed," but the uploaded photo shows an unpaved mud track.

### The Core Idea: An Automated "Pre-Disbursement Checkpoint"
**PramanSetu** acts as an automated forensic firewall. 

> **The Airport Security Analogy:**
> Think of PramanSetu like the security checkpoint at an airport. Before a passenger (the milestone claim) is allowed to board the airplane (the state treasury payment release), their luggage and boarding pass are scanned across multiple independent detectors: metal detector, X-ray machine, explosive residue swab, and passport passport chip validator. 
> 
> PramanSetu does the exact same thing for public works claims: before money leaves the treasury, it scans the photographic evidence across **ten independent mathematical, geographic, and chronological forensic vectors**.

```
[Contractor Submits Milestone Photo & Metadata]
                       │
                       ▼
    ┌─────────────────────────────────────┐
    │     10 Multi-Modal Forensic Scans   │
    │  pHash, Web, GPS, Satellite, Labor, │
    │  Material, AI Vision, NOAA, EXIF... │
    └──────────────────┬──────────────────┘
                       │
                       ▼
        [Direct Additive Risk Scorer]
        (Points summed from 250-pt pool,
             clamped to 0 - 100)
                       │
                       ▼
       ┌───────────────┴───────────────┐
       ▼               ▼               ▼
     CLEAR          REVIEW          FLAGGED
    (0 - 24)       (25 - 59)       (60 - 100)
       │               │               │
  Routine Pay     Physical Check   GFR 175 Hold
                       │
                       ▼
    [Auto-Drafted GFR 175 Show-Cause Dossier]
                       │
                       ▼
   [Deterministic SHA-256 Canonical JSON Seal]
                       │
                       ▼
     [Committed to Persistent SQLite Ledger]
                       │
                       ▼
   [Public Verification & Citizen RTI Gateway]
```

---

# 2. The Story of One Audit: Step-by-Step

To see how all the pieces connect, let's follow a single realistic audit from start to finish.

### Step 1: The Claim Arrives
A field engineer or Drawing & Disbursing Officer (DDO) opens the **Forensic Scrutiny Terminal** (`/intake`). They receive a contractor claim for "Rural Varanasi Bituminous Road Package 01" under the Pradhan Mantri Gram Sadak Yojana (PMGSY), claiming ₹45,00,000 for laying asphalt.

### Step 2: Input & Image Upload
The engineer selects the photo and enters the coordinates where the road was supposed to be built (Latitude `25.3176°N`, Longitude `82.9739°E`).

### Step 3: Clicking "Execute 10-Vector Forensic Scrutiny"
When the user clicks the button:
1. The browser wraps the image, GPS numbers, and project fields into a standard `FormData` bundle.
2. It attaches a digital visitor pass (an **HS256 Bearer JWT token**) to prove the user is an authorized officer.
3. The request is sent to the FastAPI backend at `http://127.0.0.1:8002/api/audit`.

### Step 4: Security & Validation Guard
Before running any math, the backend security layer kicks in:
* **Rate Limiter:** Checks that this IP hasn't fired more than 60 requests in the last minute.
* **Role Check (RBAC):** Verifies the JWT token belongs to an `EVALUATOR`, `DDO`, `CVO`, or `ADMIN`.
* **Magic-Byte Inspection:** Reads the first 4 bytes of the uploaded file. If someone renamed a malicious script `exploit.php` to `photo.jpg`, the server detects that the header doesn't start with `FF D8 FF` (JPEG magic bytes) and immediately rejects it.

### Step 5: Ten Forensic Engines Run in Parallel
The backend executes 10 Python modules:
* **Engine 1 (pHash):** Computes a 64-bit Discrete Cosine Transform fingerprint. It discovers this exact photo was already submitted in 2023 for a different water pipeline! (Hamming Distance = 0). **Triggered (+40 points)**.
* **Engine 2 (Web Scrape):** Checks against stock photography indexes. **Clear (0 points)**.
* **Engine 3 (GPS Telemetry):** Compares the claimed site in Varanasi against the EXIF metadata inside the photo (which was actually snapped in New Delhi, 580 km away!). **Triggered (+35 points)**.
* **Engines 4 to 10:** Checks satellite anomaly zones, muster rolls, surface materials, solar elevation, image focus, and AI tamper cues.

### Step 6: Risk Calculation
The scoring engine sums the triggered weights:
$$\text{Total} = 40 + 35 = 75 \text{ points}$$
Because $75 \ge 60$, the system automatically assigns the verdict **FLAGGED**.

### Step 7: Legal Dossier & Cryptographic Sealing
The report engine drafts an administrative **Show-Cause Notice** citing General Financial Rules (GFR 2017) Rule 175 and prepares a payment-hold recommendation. 

Then, the cryptographic service serializes the entire dossier into a standardized (canonical) JSON string and computes a **SHA-256 Integrity Seal** (e.g., `e3b0c44298fc1c149afbf4c8...`).

### Step 8: Persistent Database Storage
The entire record is written to the SQLite database (`backend/data/civicaudit.db`). It is permanently saved. Even if the server crashes or reboots, the audit, score, and seal are preserved.

### Step 9: What the User Sees
Within ~1.5 seconds, the screen updates with a glowing red risk gauge (`75 / 100`), red warning cards for the triggered vectors, the auto-drafted legal notice, and a QR code linking to the verification portal.

---

# 3. Complete Application Map: The 7 Routes

PramanSetu is organized into 7 distinct routes. Here is what every route is designed to do:

| Route | Page Name | Primary User | What It Does |
| :--- | :--- | :--- | :--- |
| [`/`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/page.tsx) | **Landing Gateway** | Public, Judges, Evaluators | Institutional context, legislative references, role selector, live health telemetry. |
| [`/intake`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/intake/page.tsx) | **Forensic Scrutiny Terminal** | Field Evaluators, DDOs | Operational form with 4 quick presets, image upload, muster roll parser, and 10-vector audit execution. |
| [`/demo`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/demo/page.tsx) | **Benchmark Evaluation Sandbox** | Judges, Reviewers, Testers | 8 standardized test scenarios covering each fraud mode in isolated `is_demo=True` mode. |
| [`/dashboard`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/dashboard/page.tsx) | **Central Vigilance Ledger** | Chief Vigilance Officers (CVO), DDOs | Persistent audit log, contractor star-ratings, repeat offender alerts, and sanitized CSV exports. |
| [`/analytics`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/analytics/page.tsx) | **Macro Vigilance Cockpit** | Vigilance Directors, Executives | Interactive GIS map, collusion network graph, March-Rush velocity curve, debarment pipeline. |
| [`/citizen`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/citizen/page.tsx) | **Social Audit & RTI Gateway** | Citizens, Gram Panchayats | Photo evidence upload, plain-language trilingual findings, and auto-generated Section 6(1) Form A RTI petitions. |
| [`/verify`](file:///c:/Users/LENOVO/OneDrive/Desktop/CivicAudit%20AI/CivicAudit%20AI/frontend/app/verify/page.tsx) | **Cryptographic Seal Validator** | General Public, Court Officers | Recomputes canonical SHA-256 seal from SQLite to verify authenticity and detect database tampering. |

---

# 4. Page-by-Page Deep Explanation

---

## PAGE 1 — Landing Command Gateway (`/`)

### First, what is this page?
Think of this as the main entrance and command center of PramanSetu. It welcomes the user, sets the legal context (GFR 2017 Rule 175), and routes users to the right tool depending on their role.

### What you see:
1. **Top Header:** National emblem seal, trilingual typography, live backend operational status pill (`● Operational` in green), and instant language selector (English / Hindi / Tamil).
2. **Hero Action Matrix:** Three large glowing cards:
   * **Launch Pre-Disbursement Scrutiny** (Blue button $\rightarrow$ `/intake`)
   * **1-Click Benchmark Suite** (Emerald button $\rightarrow$ `/demo`)
   * **Macro Vigilance Cockpit** (Purple button $\rightarrow$ `/analytics`)
3. **Four-Step Visual Pipeline:** Intake $\rightarrow$ 10-Vector Scan $\rightarrow$ Risk Score $\rightarrow$ Legal Dossier.
4. **Persona Gateway Grid:** 4 cards explaining capabilities for Citizen, Evaluator, DDO, and CVO.

### What happens behind the scenes:
* The page checks `GET /api/health` to confirm the FastAPI backend is responsive.
* If the user selects **हिंदी** or **தமிழ்**, the `LanguageContext` re-renders all text instantaneously without a full page reload and stores the preference in the browser's `localStorage`.

---

## PAGE 2 — Pre-Disbursement Forensic Intake (`/intake`)

### First, what is this page?
This is the heart of the operational system. It is where engineers, auditors, and disbursing officers evaluate real milestone claims.

### The 4 Quick-Presets:
To make demonstration fast and reproducible, the top of the page features 4 one-click presets:
1. **1. Clean PMGSY Road:** Genuine rural road; matching GPS coordinates (`25.3176°N, 82.9739°E`); all 10 vectors pass $\rightarrow$ Score `0-10 (CLEAR)`.
2. **2. Reused Asset Recycling:** Recycled 2023 pipeline photo submitted for a 2024 claim $\rightarrow$ Vector 1 triggers $\rightarrow$ Score `85-95 (FLAGGED)`.
3. **3. 580km Location Mismatch:** Claimed site in Varanasi, but photo EXIF proved it was taken in Delhi $\rightarrow$ Vector 3 triggers $\rightarrow$ Score `75-85 (FLAGGED)`.
4. **4. Ghost Labor Muster Roll:** 31 claimed workers on roll, 0 on-site faces, fake Aadhaar numbers failing Verhoeff D5 algorithm $\rightarrow$ Vector 5 triggers $\rightarrow$ Score `80-90 (FLAGGED)`.

### Every Input Field Explained:
* **Evidence Image Upload:** Accepts JPEG, PNG, WebP up to 15MB. Renders an instant canvas preview.
* **Project Name & Scheme:** Identifies the public work (e.g., PMGSY, Jal Jeevan Mission, Smart Cities).
* **Contractor Name:** Matches against registered vendors in SQLite.
* **Claim Amount (₹):** The invoice amount being evaluated for disbursement.
* **Claimed Latitude & Longitude:** The exact WGS-84 coordinates where the physical asset is supposed to exist.
* **Claimed Material:** The milestone stage (e.g., "100% Asphalt Bituminous Pavement", "RCC Slab", "PCC Bedding").
* **Labor Muster Roll (CSV):** Uploads tabular daily labor logs for Aadhaar checksum verification.

### What happens when you click "Execute 10-Vector Forensic Scrutiny"?
1. **Frontend:** Synthesizes the canvas blob and metadata into a `FormData` object.
2. **API Call:** Sends `POST /api/audit` with an `Authorization: Bearer <JWT>` header.
3. **Backend Execution:** 10 Python forensic services analyze the payload.
4. **Scoring:** Points are calculated by `scoring_service.py` and clamped between 0 and 100.
5. **Dossier Compilation:** `report_service.py` generates the GFR 175 show-cause notice and UUID dossier ID.
6. **Crypto Sealing:** `crypto_service.py` serializes canonical JSON and computes the SHA-256 digest.
7. **SQLite Persistence:** Inserts the audit row into `civicaudit.db`.
8. **UI Render:** The results section smoothly expands with:
   * A circular risk gauge (Green for Clear, Amber for Review, Red for Flagged).
   * 10 forensic vector status cards with triggered badges and technical evidence.
   * Auto-drafted GFR 175 Administrative Show-Cause Notice.
   * **Software Keyed HMAC Signature Stamp** button to apply officer sign-off.

---

## PAGE 3 — Benchmark Evaluation Sandbox (`/demo`)

### First, what is this page?
This is a dedicated evaluative sandbox containing **8 standardized test scenarios**. It allows evaluators, judges, and reviewers to test every failure mode of the 10 forensic algorithms without affecting real contractor ratings.

### The 8 Standardized Scenarios:

| # | Scenario Title | Primary Failure Mode Tested | Expected Score & Verdict |
| :--- | :--- | :--- | :--- |
| **1** | **Authentic Infrastructure** | Clean physical progress, matching coordinates, verified telemetry | `0 – 10 (CLEAR)` |
| **2** | **Past Reused Asset Recycling** | Recycled 2023 pipeline photo (64-bit DCT pHash distance = 0) | `85 – 95 (FLAGGED)` |
| **3** | **580km Location Mismatch** | Photo GPS in Delhi, claimed project site in Varanasi | `75 – 85 (FLAGGED)` |
| **4** | **Web Stock Photo Theft** | Stock image stolen from Shutterstock database | `80 – 90 (FLAGGED)` |
| **5** | **Ghost Labor & Muster Roll** | 31 claimed workers; invalid Aadhaar Verhoeff D5 checksums | `80 – 90 (FLAGGED)` |
| **6** | **Material Milestone Mismatch** | Finished asphalt claimed on raw dirt/mud track | `65 – 75 (FLAGGED)` |
| **7** | **Chrono & Weather Anomaly** | Direct bright sunlight claimed during heavy monsoon rainfall | `55 – 65 (FLAGGED)` |
| **8** | **Sub-2KB Degraded Payload** | Severely downscaled thumbnail with stripped metadata | `35 – 45 (REVIEW)` |

### Demo Data Isolation (`is_demo=True`):
When a scenario is run from `/demo`, the request transmits `is_demo=True`. The backend persists the audit as `audit_type='DEMO'` and **does not deduct points from the contractor's real integrity scorecard**, keeping the production ledger clean.

---

## PAGE 4 — Central Vigilance Ledger (`/dashboard`)

### First, what is this page?
The persistent repository of all completed audits, contractor scorecards, repeat-offender alerts, and sanitized data export tools.

### Key Features:
1. **Contractor Integrity Leaderboard:** Displays contractor names, dynamic trust ratings (0–100%), star ratings (1.0–5.0), past violation counts, and repeat-offender warning badges.
2. **Audit History Table:** Lists dossier IDs, project names, risk scores, verdicts, record types (`REAL` vs `DEMO`), and SHA-256 integrity confirmation badges (`MATCH_CONFIRMED`).
3. **Search & Filter:** Real-time filtering by contractor name, scheme, or verdict (`CLEAR` / `REVIEW` / `FLAGGED`).
4. **Formula-Safe CSV Export:** The **Export CSV** button downloads all audit records. To protect users from spreadsheet vulnerabilities, the export runs through `escapeCsvCell()`, prepending a single quote (`'`) to any cell starting with `=`, `+`, `-`, `@`, `\t`, or `\r`.

---

## PAGE 5 — Macro Vigilance Cockpit & Analytics (`/analytics`)

### First, what is this page?
An executive oversight dashboard designed for Chief Vigilance Officers (CVO) to detect regional corruption patterns, cartel collusion, and fiscal year-end spending spikes.

### The 4 Analytics Views:
1. **1. GIS Fraud Heatmap:** An interactive Leaflet map rendering live OpenStreetMap tiles. It plots dynamic project markers from the SQLite database alongside red circular **Anomaly Fraud Zones** (e.g., Prayagraj, Yamuna Floodplain, Patna).
2. **2. Contractor Collusion Syndicate Network:** An interactive topological graph mapping shared directors, phone numbers, and joint bank accounts across bidding syndicates.
3. **3. March-Rush Expenditure Velocity:** A multi-month spending bar chart highlighting the annual Q4 spike where fraudulent claims jump by 3.8x baseline volume.
4. **4. Inter-Departmental Debarment Pipeline:** Case tracking table showing proceedings from GFR 175 show-cause notices to Performance Bank Guarantee (PBG) seizures and GeM portal blacklisting.

---

## PAGE 6 — Citizen Social Audit & RTI Gateway (`/citizen`)

### First, what is this page?
Empowers grassroots citizens, village social audit committees, and RTI activists to inspect public works and demand accountability without legal expertise.

### How it works:
1. **Citizen Upload:** A villager uploads an on-site photo and enters the project name, panchayat, and inspection notes.
2. **Instant Plain-Language Finding:** The backend analyzes the photo and returns an easily understandable card in Hindi, Tamil, or English (e.g., *"Photo shows unpaved mud road, but contractor claimed 100% completion"*).
3. **Automated Section 6(1) Form A RTI Petition:** The system auto-generates a formatted legal RTI application pre-filled with the Public Information Officer (PIO) address, project details, and a dynamic **30-day statutory response deadline countdown**.
4. **Print / Copy:** The citizen can copy the text or click **Print Petition** to generate a clean, physical submission document.

---

## PAGE 7 — Public Cryptographic Seal Validator (`/verify`)

### First, what is this page?
A public authenticity verification portal where anyone (a citizen, journalist, or court officer) can input a Dossier ID to verify that a government audit report is genuine and has not been altered in the database.

### The 3 Verification Outcomes:

```
                  [User Inputs Dossier ID]
                             │
                             ▼
                 [Query SQLite civicaudit.db]
                             │
            ┌────────────────┴────────────────┐
            │                                 │
      [Row Found]                       [Row Not Found]
            │                                 │
    [Canonicalize JSON]                       ▼
    [Recompute SHA-256]               HTTP 404 Not Found
            │                         (Red "Missing ID" Box)
    ┌───────┴────────┐
    ▼                ▼
[Hashes Match]   [Hashes Differ]
    │                │
    ▼                ▼
200 OK (Green)   200 OK (Red)
"Authentic Seal" "Tamper Detected"
```

1. **Authentic Verified (Green Certificate):** The recomputed SHA-256 hash matches the stored seal. Ledger integrity is confirmed unaltered.
2. **Dossier Not Found (HTTP 404 Red Banner):** The entered ID does not exist in the database.
3. **Tamper Detected (Red Warning Banner):** The database row was altered after the initial audit, causing the recomputed SHA-256 hash to mismatch the stored seal.

---

# 5. The Ten Forensic Vectors: Explained Like a Friend

Every claim is evaluated across **10 independent scoring engines**. Here is exactly how each engine works:

---

### Vector 1: Perceptual Image Hashing (pHash) — Asset Recycling
* **In one sentence:** Catches contractors who submit the same photo across multiple claims or years.
* **Everyday Analogy:** Think of pHash like a human fingerprint. Even if you resize the image, slightly crop it, or adjust the brightness, the overall structure (the fingerprint) remains identical.
* **Technical Algorithm:** Converts the photo to grayscale, resizes to $32 \times 32$, computes a 2D Discrete Cosine Transform (DCT), and generates a 64-bit binary fingerprint. It compares this against past submissions using **Hamming Distance**.
* **Trigger Threshold:** Hamming Distance $\le 5$ bits.
* **Weight Contribution:** **40 Risk Points**.

---

### Vector 2: Web Reverse Image Search — Stock Photo Theft
* **In one sentence:** Catches contractors who steal photos from Google, Shutterstock, or Wikipedia instead of visiting the real site.
* **Everyday Analogy:** Like Google Reverse Image Search running inside the auditor's terminal.
* **Technical Algorithm:** Computes dense image feature vectors and measures cosine similarity against a database of indexed internet construction photos.
* **Trigger Threshold:** Feature Cosine Similarity $\ge 0.85$.
* **Weight Contribution:** **40 Risk Points**.

---

### Vector 3: Geodesic Spatial Distance Check — Off-Site Photography
* **In one sentence:** Checks if the photo was taken at the actual project site or somewhere hundreds of kilometers away.
* **Everyday Analogy:** If a contractor says they paved a road in Varanasi, but the smartphone GPS records the photo in New Delhi, the claim is clearly fraudulent.
* **Technical Algorithm:** Extracts EXIF GPS tags from the photo and calculates the geodesic distance to the claimed site using the **WGS-84 Vincenty / Haversine formula**.
* **Trigger Thresholds:**
  * $\le 500\text{ m}$: `MATCH` (0 points).
  * $500\text{ m} - 1500\text{ m}$: `REVIEW` (Warning, 0 mismatch points).
  * $> 1500\text{ m}$: `MISMATCH` (**+35 Risk Points**).

---

### Vector 4: Satellite Ground-Truth Anomaly Zones
* **In one sentence:** Cross-references GPS coordinates with known environmental hazard perimeters and restricted floodplains.
* **Everyday Analogy:** Like a GPS fence warning you that the claimed construction site is actually in the middle of a riverbed.
* **Technical Algorithm:** Ray-casting **Point-in-Polygon (PIP)** geospatial algorithm against defined anomaly coordinates (e.g., active floodplains).
* **Trigger Threshold:** Coordinate point falls inside an active anomaly polygon.
* **Weight Contribution:** **30 Risk Points**.

---

### Vector 5: Ghost Labor Muster Roll & Aadhaar Checksum
* **In one sentence:** Detects fake workers, duplicate names, and fabricated Aadhaar numbers on daily labor rolls.
* **Everyday Analogy:** Like a bank verifying that a credit card number follows a mathematical formula before accepting a transaction.
* **Technical Algorithm:** Parses CSV muster rolls, validates worker Aadhaar numbers using the **Verhoeff D5 dihedral group algorithm** (the official UIDAI checksum), and flags wage payouts exceeding statutory caps.
* **Trigger Threshold:** Checksum failure rate $> 15\%$ or wage discrepancies.
* **Weight Contribution:** **30 Risk Points**.

---

### Vector 6: Visual Milestone Material Classifier
* **In one sentence:** Verifies that the physical material visible in the photo matches what the contractor billed for.
* **Everyday Analogy:** If the invoice says "Finished Bituminous Asphalt" but the photo shows unpaved mud and dirt, the machine flags the mismatch.
* **Technical Algorithm:** Softmax probability distribution over material classes (`Asphalt Road`, `Mud Track`, `Concrete Pavement`, `Excavation Trench`).
* **Trigger Threshold:** Claimed material does not match detected surface.
* **Weight Contribution:** **25 Risk Points**.

---

### Vector 7: Multimodal AI Vision Tamper Analysis
* **In one sentence:** Uses advanced AI vision to spot digital manipulations, Photoshop edits, and AI-generated image artifacts.
* **Everyday Analogy:** An experienced forensic photo examiner inspecting pixel lighting, shadows, and clone stamps.
* **Technical Algorithm:** Google Gemini 2.0 Flash Vision API analyzing visual cues, with automatic fallback to **Shannon Entropy gradient variance** when offline.
* **Trigger Threshold:** AI confidence score $\ge 0.70$ indicating synthetic or tampered cues.
* **Weight Contribution:** **20 Risk Points**.

---

### Vector 8: Chrono-Solar & Weather Forensics
* **In one sentence:** Verifies whether the sun position and weather in the photo match the claimed date and time.
* **Everyday Analogy:** If a contractor claims a photo was taken at 2:00 PM on a bright July afternoon, but the shadows show the sun is at a morning angle or the sky is cloudless during a recorded torrential monsoon downpour, the timestamp is fake.
* **Technical Algorithm:** **NOAA Solar Position Algorithm (SPA)** computes the solar elevation angle $\alpha$ and azimuth $\theta$ for the exact timestamp and coordinates.
* **Trigger Threshold:** Solar angle discrepancy $> 15^\circ$ or weather mismatch.
* **Weight Contribution:** **15 Risk Points**.

---

### Vector 9: EXIF Hardware GPS Integrity Check
* **In one sentence:** Flags photos that have had their camera metadata deliberately stripped or scrubbed.
* **Everyday Analogy:** Like an unsigned official document missing its government seal and timestamp.
* **Technical Algorithm:** Scans the binary EXIF header for camera make, model, timestamp, and GPS IFD blocks.
* **Trigger Threshold:** GPS coordinates missing or EXIF header completely stripped.
* **Weight Contribution:** **10 Risk Points**.

---

### Vector 10: Image Quality & Deliberate Blur Detection
* **In one sentence:** Detects severely blurred or downscaled photos submitted intentionally to hide shoddy construction work.
* **Everyday Analogy:** If a student submits an illegible, smeared exam paper so the teacher can't see the wrong answers.
* **Technical Algorithm:** Computes the **Laplacian focus variance** ($\sigma^2$) across high-frequency edges.
* **Trigger Threshold:** $\sigma^2 < 100$ (severe blur) or file size $< 2\text{ KB}$.
* **Weight Contribution:** **5 Risk Points**.

---

# 6. The 250-Point Additive Scoring Model

### Why 250 Total Capacity?
The system has 10 vectors with weights adding up to 250 points:
$$40 + 40 + 35 + 30 + 30 + 25 + 20 + 15 + 10 + 5 = 250 \text{ points}$$

Why not 100? Because in high-stakes public procurement fraud, multiple catastrophic violations often occur simultaneously (e.g., a recycled photo + 500 km location mismatch + fake muster roll = $40 + 35 + 30 = 105$ points). The 250-point capacity ensures that every vector has full mathematical weight.

### The Clamped Formula:
$$\text{Total Score} = \sum_{i=1}^{10} \text{Weight}_i \times \mathbb{I}(\text{Vector}_i = \text{TRIGGERED})$$
$$\mathbf{\text{Final Risk Score}} = \mathbf{\min(100, \max(0, \text{Total Score}))}$$

### The Three Decision Thresholds:

```
[0 ───────────────── 24] ───► CLEAR    (Approved for routine treasury release)
[25 ──────────────── 59] ───► REVIEW   (Provisional hold: requires physical field re-inspection)
[60 ─────────────── 100] ───► FLAGGED  (Payment hold: auto-drafts GFR 175 Show-Cause Directive)
```

### Worked Calculation Examples:
* **Example A (Single Moderate Issue):** Missing GPS metadata triggers Vector 9 (+10 points). 
  $$\text{Total} = 10 \rightarrow \text{Final} = 10 \rightarrow \mathbf{CLEAR}$$
* **Example B (Material Mismatch):** Asphalt claimed on mud triggers Vector 6 (+25 points).
  $$\text{Total} = 25 \rightarrow \text{Final} = 25 \rightarrow \mathbf{REVIEW}$$
* **Example C (Major Fraud):** Reused asset (+40) and 580km GPS mismatch (+35).
  $$\text{Total} = 75 \rightarrow \text{Final} = 75 \rightarrow \mathbf{FLAGGED}$$
* **Example D (Catastrophic Multi-Vector Fraud):** Vectors 1 (+40), 2 (+40), 3 (+35), 5 (+30), and 6 (+25) all trigger.
  $$\text{Total} = 170 \rightarrow \text{Final} = \min(100, 170) = \mathbf{100 \ (FLAGGED)}$$

---

# 7. Security, Authentication & Cryptography

---

### Authentication & Passwords
* **Password Hashing:** Uses **PBKDF2-HMAC-SHA256** with 100,000 iterations and a cryptographically secure 16-byte random salt. Plaintext passwords are never stored.
* **JWT Tokens:** When an officer logs in, the backend issues an **HS256-signed Bearer JWT** valid for 24 hours. The token contains the user's role (`EVALUATOR`, `DDO`, `CVO`, `ADMIN`, `CITIZEN`).
* **Logout:** Client-side token disposal. The frontend removes the token from memory and `localStorage`.

### 401 Unauthorized vs. 403 Forbidden
* **401 Unauthorized:** The user has not provided a valid token (not logged in or token expired).
* **403 Forbidden:** The user is logged in, but their role lacks permission (e.g., a `CITIZEN` attempting to call the officer-only `/api/pki/sign` endpoint).

### Sliding-Window Rate Limiting
To prevent Denial of Service (DoS) attacks and external AI wallet depletion, an in-memory token bucket limits requests:
* Audits: 60 requests / minute.
* Citizen Reports: 30 requests / minute.
* Public Verifications: 120 requests / minute.
* *If exceeded:* Returns `HTTP 429 Too Many Requests` with a `Retry-After: 30` header.

### File Upload Hardening
* Files are capped at **15 MB**.
* The server reads binary magic bytes (`FF D8 FF` for JPEG, `89 50 4E 47` for PNG, `52 49 46 46` for WebP). Renaming `malicious.exe` to `photo.jpg` is immediately blocked.

### What SHA-256 Does (and Does NOT) Guarantee
* **What it DOES guarantee:** If a database row is modified by even one character (e.g., changing a Risk Score from `75` to `20`), the recomputed SHA-256 seal will change completely, instantly exposing the tampering.
* **What it does NOT guarantee:** SHA-256 is a symmetric cryptographic digest, not an asymmetric hardware digital signature. It proves *data consistency*, but if a rogue database administrator alters both the record and the stored seal at the exact same moment, SHA-256 alone cannot detect it without an external immutable timestamp ledger.

---

# 8. Real Implementation vs. Demo / Simulated Truth Matrix

To ensure absolute technical honesty, here is the official classification of every capability:

| Feature / Component | Technical Reality in Source Code | Official Classification |
| :--- | :--- | :--- |
| **10 Python Forensic Engines** | Genuine OpenCV, NumPy, WGS-84, NOAA SPA, and Verhoeff D5 math | **REAL IMPLEMENTATION** |
| **Composite Risk Scoring (0–100)** | Direct additive accumulator clamped from 250-pt capacity | **REAL IMPLEMENTATION** |
| **Persistent SQLite Storage** | ACID-compliant storage in `backend/data/civicaudit.db` | **REAL IMPLEMENTATION** |
| **Deterministic SHA-256 Seal** | Canonical JSON serialization and recomputed digest check | **REAL IMPLEMENTATION** |
| **JWT Auth & Backend RBAC** | HS256 tokens and `require_roles` route guards | **REAL IMPLEMENTATION** |
| **Sliding-Window Rate Limiter** | In-memory token bucket per IP / user identity | **REAL IMPLEMENTATION** |
| **CSV Formula Injection Defense** | `escapeCsvCell()` single-quote prepender | **REAL IMPLEMENTATION** |
| **Trilingual Localization Engine** | React Context + persistent `localStorage` (EN / HI / TA) | **REAL IMPLEMENTATION** |
| **Section 6(1) Form A RTI Generator** | Auto-filled legal petition with 30-day statutory countdown | **REAL IMPLEMENTATION** |
| **Software PKI Signature Adapter** | Keyed HMAC-SHA256 signature stamp generator | **DEVELOPMENT ONLY** |
| **Hardware PKCS#11 USB Token** | Uninstantiated driver wrapper interface | **NOT IMPLEMENTED** |
| **Treasury Fund Freeze** | Auto-drafts GFR 175 administrative notice (not direct PFMS call) | **SIMULATED / ADVISORY** |
| **Historical Claims Database** | `backend/mock_db.json` (5 static benchmark cases) | **MOCK / REFERENCE** |
| **Web Stock Photo Index** | `backend/mock_web_db.json` (3 static benchmark cases) | **MOCK / REFERENCE** |
| **Collusion Syndicate Graph** | Curated topological SVG network in analytics | **STATIC DEMO** |
| **Multimodal AI Vision** | Google Gemini 2.0 Flash REST API | **EXTERNAL DEPENDENCY** |
| **Offline Visual Fallback** | Local Shannon Entropy gradient variance analyzer | **REAL IMPLEMENTATION** |

---

# 9. A Full Day in the Life: Evaluator Rahul

To see how PramanSetu works in practice, let’s follow a day in the life of **Rahul**, a Sub-Divisional Engineer in Uttar Pradesh:

* **09:30 AM — Receiving the Claim:** Rahul logs in as an `EVALUATOR`. He receives an invoice for ₹42,50,000 for a rural drinking water pipeline in Prayagraj under the Jal Jeevan Mission.
* **09:45 AM — Running Scrutiny on `/intake`:** Rahul enters the project details, sets the claimed GPS coordinates, and uploads the contractor's milestone photo. He clicks **Execute 10-Vector Forensic Scrutiny**.
* **09:47 AM — The Flag:** The screen flashes **Risk Score: 92 (FLAGGED)**. Engine 1 detects that the photo has a Hamming Distance of `0`—it is identical to a photo submitted in 2023 for a different project.
* **10:00 AM — Drafting the Directive:** PramanSetu compiles an administrative Show-Cause Notice citing GFR 2017 Rule 175. Rahul clicks **Apply Software Signature Stamp**, sealing the dossier with ID `DOSSIER-202608-PRY-02`.
* **11:30 AM — CVO Oversight on `/analytics`:** The Chief Vigilance Officer opens the Macro Cockpit. The Prayagraj case appears as an active red hotspot on the GIS map. The Collusion Graph highlights that the same contractor is bidding under two sister companies.
* **02:00 PM — Citizen Social Audit on `/citizen`:** In the village, a resident uses the Citizen Portal to upload a photo of the dry pipeline. The system confirms the incomplete work and generates a pre-filled Section 6(1) Form A RTI application.
* **04:00 PM — Public Verification on `/verify`:** The citizen types `DOSSIER-202608-PRY-02` into the verification portal. The green certificate appears, confirming that the payment hold was officially registered in the vigilance ledger.

---

# 10. Master Interaction Table: Every Button & Click

| Page | Button / Control | User Action | Frontend State | API Endpoint | Backend Service | Database Action | Final UI Update |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Header** | Language Selector | Click `हिंदी` / `தமிழ்` | Updates `language` state | None (Local) | None | Persists to `localStorage` | Re-renders all text instantly |
| **Header** | Health Telemetry Pill | Automatic on load | Polls health status | `GET /api/health` | `main.py` | None | Displays green `Operational` pill |
| **`/intake`** | Preset Card (1–4) | Click preset card | Populates form & canvas | None (Local) | None | None | Form fields & image preview fill |
| **`/intake`** | Execute Audit | Click submit button | Sets `isLoading=true` | `POST /api/audit` | 10 Forensic Engines + Scorer | `INSERT INTO audits` | Displays risk gauge & dossier |
| **`/intake`** | Apply DSC Stamp | Click signature button | Attaches stamp | `POST /api/pki/sign` | `pki_service.py` | `UPDATE audits` | Shows signed cryptographic block |
| **`/demo`** | Benchmark Scenario (1–8) | Click scenario button | Transmits demo payload | `POST /api/audit` | 10 Engines (`is_demo=True`) | `INSERT INTO audits (audit_type='DEMO')` | Shows score; preserves ratings |
| **`/dashboard`** | Export CSV | Click export button | Sanitizes formula cells | `GET /api/audits` | `main.py` | `SELECT FROM audits` | Downloads `.csv` file to disk |
| **`/dashboard`** | Search / Filter | Type in search box | Filters `audits` array | None (Local) | None | None | Table filters rows in real time |
| **`/analytics`** | Tab Switcher (1–4) | Click tab button | Sets `activeTab` | `GET /api/analytics/*` | `analytics_service.py` | `SELECT FROM audits` | Renders Map, Graph, or Charts |
| **`/citizen`** | Submit Evidence | Click submit report | Sets submitting state | `POST /api/citizen/report` | `citizen_service.py` | `INSERT INTO citizen_reports` | Displays RTI Form A & countdown |
| **`/citizen`** | Copy / Print Petition | Click copy/print | Copies to clipboard / Print | None (Local) | None | None | Opens browser print dialog |
| **`/verify`** | Verify Seal | Input ID & click verify | Sets checking state | `GET /api/verify/{id}` | `crypto_service.py` | `SELECT FROM audits WHERE id=?` | Shows Green, 404, or Tampered box |

---

# 11. Troubleshooting: What Happens When Things Go Wrong?

| Symptom / Error | What Caused It | What You See on Screen | Immediate Fix |
| :--- | :--- | :--- | :--- |
| **HTTP 401 Unauthorized** | Missing, expired, or invalid Bearer JWT token | Red error toast: *"Unauthorized"* | Log in via the demonstration environment to refresh your session token. |
| **HTTP 403 Forbidden** | Authenticated user lacks required role permissions | Red banner: *"Forbidden: Insufficient role"* | Switch to an officer account with `DDO`, `CVO`, or `ADMIN` permissions. |
| **HTTP 404 Not Found** | Entered Dossier ID does not exist in SQLite | Red box: *"Dossier Not Found (404)"* | Check the Dossier ID from the Ledger on `/dashboard` and re-enter. |
| **HTTP 413 Payload Too Large** | Uploaded image exceeds 15 MB cap | Upload error: *"File exceeds 15MB"* | Resize or compress the photo before uploading. |
| **HTTP 429 Too Many Requests** | Exceeded sliding-window rate limit (60/min) | Toast: *"Rate limit exceeded (429)"* | Wait 30 seconds for the token bucket to replenish. |
| **Backend Offline (Degraded Pill)** | FastAPI server on port 8002 is stopped | Header pill turns Amber: `● Degraded` | Restart backend using `python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload`. |
| **Gemini AI Offline / No Key** | `GEMINI_API_KEY` missing from `.env` | Scrutiny finishes without error | System automatically runs local Shannon Entropy gradient fallback. |
| **Corrupted Image Upload** | File is missing valid binary magic bytes | Error: *"Invalid image payload format"* | Ensure the uploaded file is a genuine JPEG, PNG, or WebP image. |
| **Verification Tamper Mismatch** | A row in `civicaudit.db` was manually altered | Red warning: *"Integrity Check Failed (ALTERED)"* | Database record was modified after sealing. Re-run an authentic audit. |

---

# 12. Beginner FAQ: 25 Common Questions Answered

1. **What is PramanSetu?**  
   An automated GovTech evidence-intelligence platform that inspects public works photos before state funds are paid out.
2. **What does the name mean?**  
   *Praman* (प्रमाण) means "Proof/Evidence" and *Setu* (सेतु) means "Bridge". It is the Bridge of Verifiable Evidence.
3. **Why are there ten forensic vectors?**  
   Because fraud takes many forms—reusing old photos, claiming the wrong location, faking labor rolls, or using stock photos. Ten vectors cover the full spectrum of physical and digital deception.
4. **What is pHash?**  
   A perceptual hash that turns an image into a 64-bit visual fingerprint. Unlike cryptographic hashes, two photos of the same road look nearly identical in pHash even if resized or compressed.
5. **What is Hamming Distance?**  
   The number of bits that differ between two pHash fingerprints. A distance of `0` means the photos are completely identical.
6. **What is EXIF metadata?**  
   Hidden technical data saved inside photos by digital cameras and smartphones, including GPS coordinates, capture date, shutter speed, and camera model.
7. **What is the Verhoeff D5 algorithm?**  
   The official mathematical checksum algorithm used by UIDAI to validate that a 12-digit Aadhaar number is mathematically valid.
8. **Why does the scoring capacity add up to 250?**  
   To allow severe simultaneous infractions to accumulate full weight before clamping to the 0–100 scale.
9. **What does FLAGGED mean?**  
   A risk score of 60 or higher, indicating severe forensic anomalies. It triggers an automatic administrative payment-hold draft under GFR 175.
10. **Does a CLEAR verdict guarantee 100% zero fraud?**  
    No automated tool can replace physical site inspections entirely. `CLEAR` means no digital, spatial, labor, or chronological anomalies were detected in the submitted evidence.
11. **Where is audit data stored?**  
    In an ACID-compliant SQLite 3 database located at `backend/data/civicaudit.db`.
12. **What happens when I reboot my computer or restart the server?**  
    Nothing is lost. All audits, citizen reports, and contractor scorecards are permanently committed to disk in SQLite.
13. **What is the difference between REAL and DEMO audits?**  
    `DEMO` audits run with `is_demo=True` to let reviewers test the system without deducting rating points from real contractors.
14. **What is a SHA-256 seal?**  
    A 256-bit cryptographic digest calculated over the canonical JSON representation of an audit dossier to detect data tampering.
15. **Is SHA-256 a digital signature?**  
    No. SHA-256 is an integrity hash. Digital signatures require public-key cryptography (like RSA or ECDSA).
16. **Does the software signature use a physical USB smartcard?**  
    In this release, it uses a software keyed HMAC stamp. Hardware PKCS#11 smartcards require physical air-gapped workstations and drivers.
17. **Does PramanSetu directly initiate bank transfers or freezes in PFMS?**  
    No. It generates administrative payment-hold directive drafts under GFR 2017 Rule 175 for Drawing & Disbursing Officers.
18. **What is CSV formula injection?**  
    A security exploit where malicious spreadsheet formulas (like `=cmd|' /C ...'`) execute when opened in Excel. PramanSetu neutralizes this by prepending `'` to trigger characters.
19. **What happens if the Gemini AI API is unreachable?**  
    The backend automatically falls back to local Shannon Entropy visual gradient analysis without throwing an error.
20. **Can citizens use PramanSetu?**  
    Yes! The Citizen Portal (`/citizen`) lets citizens submit photos and automatically drafts a Section 6(1) Form A RTI petition.
21. **What is the 30-day RTI countdown?**  
    Under Section 7(1) of the RTI Act 2005, the Public Information Officer (PIO) has exactly 30 calendar days to respond to citizen information requests.
22. **What is the March-Rush anomaly?**  
    A well-documented phenomenon where government departments rush to exhaust annual budgets before March 31, leading to a 3.8x spike in fraudulent claims.
23. **How does rate limiting protect the application?**  
    It prevents automated bots from flooding the server with thousands of heavy image processing requests.
24. **How do I switch languages?**  
    Click the language selector in the top header to instantly switch between English, Hindi (हिंदी), and Tamil (தமிழ்).
25. **What is the official classification of this release?**  
    **B — Production-Capable Single-Node Deployment**.

---

# 13. If You Only Remember 10 Things

1. **PramanSetu is a Pre-Disbursement Checkpoint:** It stops fraudulent infrastructure claims *before* funds leave the state treasury.
2. **Ten Independent Vectors:** It analyzes evidence across 10 mathematical, spatial, and chronological engines.
3. **Additive Scoring System:** Vectors add points from a 250-point capacity, clamped between 0 and 100.
4. **Clear Decision Rules:** $0-24 = \text{CLEAR}$, $25-59 = \text{REVIEW}$, $60-100 = \text{FLAGGED}$.
5. **Auto-Drafted Legal Notices:** Flags trigger administrative payment-hold directives citing GFR 2017 Rule 175.
6. **ACID SQLite Persistence:** Audits are permanently saved in `backend/data/civicaudit.db` and survive server restarts.
7. **Deterministic SHA-256 Sealing:** Recomputes hash seals on `/verify` to detect any database tampering.
8. **Demo Isolation:** Testing benchmark scenarios on `/demo` never corrupts live contractor ratings.
9. **Grassroots Citizen RTI:** Auto-generates statutory Section 6(1) RTI petitions with a 30-day PIO deadline.
10. **Technically Honest:** Clearly separates real algorithms from software PKI prototypes and reference datasets.
