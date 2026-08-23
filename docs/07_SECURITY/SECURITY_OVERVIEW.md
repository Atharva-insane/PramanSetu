# 🔒 PramanSetu Security & Cryptographic Architecture

1. **Pre-Execution Magic Byte Validation**: Inspects binary file signatures to block disguised executables (`MZ`, `ELF`).
2. **Sliding-Window Rate Limiting**: In-memory token bucket limits public requests to 10/min and authenticated requests to 60/min.
3. **Deterministic SHA-256 Seals**: Canonical JSON serialization ensures audit dossiers are tamper-evident.
4. **XSS & Injection Protection**: React DOM automatically escapes HTML entities; parameterized SQLite queries prevent SQL injection.
5. **Citizen Anonymity Guarantee**: No citizen names, phone numbers, or email addresses are stored in the database.
