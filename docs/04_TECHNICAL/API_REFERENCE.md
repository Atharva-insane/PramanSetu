# 📡 PramanSetu REST API Specification

| HTTP Method | Route | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/audit` | Execute full multi-vector forensic audit on project evidence | Optional Bearer JWT |
| `POST` | `/api/citizen/report` | Execute citizen social audit & auto-generate Section 6(1) Form A RTI | No (Public Gateway) |
| `GET` | `/api/citizen/reports` | Retrieve recent citizen social audit records (`limit=1..200`) | No (Public Registry)|
| `GET` | `/api/audits` | Retrieve persistent audit ledger records | Optional Bearer JWT |
| `GET` | `/api/analytics` | Compute dynamic Macro Vigilance aggregate KPIs and geo-audits | No |
| `GET` | `/api/verify/{dossier_id}` | Verify cryptographic SHA-256 tamper seal of issued dossier | No (Public QR Verify)|
| `POST` | `/api/auth/login` | Authenticate vigilance officer & issue HS256 JWT Bearer token | No |
| `GET` | `/api/health` | Healthcheck and subsystem diagnostics | No |
