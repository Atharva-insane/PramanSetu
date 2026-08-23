# 💾 PramanSetu Database Architecture

- **Engine**: SQLite 3 (Single-Node ACID Storage with WAL mode enabled).
- **Location**: `backend/civicaudit.db`.

### Core Tables:
1. **`audits`**: Complete record of all institutional procurement audits, risk scores, verdicts, and raw JSON payloads.
2. **`citizen_reports`**: Public social audit records, audit IDs, project names, observation notes, risk scores, and verdicts.
3. **`contractors`**: Dynamic vendor registry tracking integrity scores ($0-100$), star ratings ($1.0-5.0$), and debarment alerts.
4. **`users`**: RBAC credentials (Super Admin, Vigilance Officer, Social Auditor) hashed with PBKDF2-HMAC-SHA256.
