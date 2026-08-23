import os
import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "data", "civicaudit.db")


def get_db_connection():
    """Returns a connection to the SQLite persistent database."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database schema and performs non-destructive column migrations."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Audits Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            dossier_id TEXT PRIMARY KEY,
            project_name TEXT,
            scheme TEXT,
            contractor_name TEXT,
            tender_id TEXT,
            claim_amount TEXT,
            claimed_latitude REAL,
            claimed_longitude REAL,
            risk_score INTEGER,
            verdict TEXT,
            decision_reason TEXT,
            recommended_action TEXT,
            sha256_seal TEXT,
            created_at_utc TEXT,
            raw_payload TEXT,
            audit_type TEXT DEFAULT 'REAL',
            created_by TEXT DEFAULT 'system',
            created_by_role TEXT DEFAULT 'EVALUATOR',
            signature_block TEXT
        )
    """)

    # Non-destructive migration for existing tables
    cursor.execute("PRAGMA table_info(audits)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "audit_type" not in columns:
        cursor.execute("ALTER TABLE audits ADD COLUMN audit_type TEXT DEFAULT 'REAL'")
    if "created_by" not in columns:
        cursor.execute("ALTER TABLE audits ADD COLUMN created_by TEXT DEFAULT 'system'")
    if "created_by_role" not in columns:
        cursor.execute("ALTER TABLE audits ADD COLUMN created_by_role TEXT DEFAULT 'EVALUATOR'")
    if "signature_block" not in columns:
        cursor.execute("ALTER TABLE audits ADD COLUMN signature_block TEXT")

    # 2. Contractors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contractors (
            contractor_id TEXT PRIMARY KEY,
            contractor_name TEXT UNIQUE,
            integrity_score INTEGER,
            star_rating REAL,
            past_violations INTEGER,
            is_repeat_offender INTEGER,
            cvo_alert TEXT,
            last_audited_at TEXT
        )
    """)

    # 3. Citizen Social Audits Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizen_reports (
            audit_id TEXT PRIMARY KEY,
            project_id TEXT,
            project_name TEXT,
            citizen_notes TEXT,
            risk_score INTEGER,
            verdict TEXT,
            created_at_utc TEXT
        )
    """)

    conn.commit()
    seed_default_contractors(cursor, conn)
    conn.close()


def seed_default_contractors(cursor, conn):
    """Seeds initial contractor database records if empty."""
    cursor.execute("SELECT COUNT(*) FROM contractors")
    count = cursor.fetchone()[0]

    if count == 0:
        now_iso = datetime.now(timezone.utc).isoformat()
        default_contractors = [
            ("CONT-001", "M/s Apex Civil Constructions Ltd.", 38, 2.0, 3, 1, "Active CVO debarment notice pending. Past asset recycling in Prayagraj & Gorakhpur.", now_iso),
            ("CONT-002", "Varanasi Highway Developers Ltd.", 94, 5.0, 0, 0, "High compliance rating. Zero forensic anomalies.", now_iso)
        ]

        cursor.executemany("""
            INSERT INTO contractors (
                contractor_id, contractor_name, integrity_score, star_rating,
                past_violations, is_repeat_offender, cvo_alert, last_audited_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, default_contractors)
        conn.commit()


def save_audit_record(
    audit_data: Dict[str, Any],
    is_demo: bool = False,
    created_by: str = "evaluator",
    created_by_role: str = "EVALUATOR",
    signature_block: Optional[Dict[str, Any]] = None
):
    """Persists a completed forensic audit record into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    dossier = audit_data.get("dossier", {}) if isinstance(audit_data.get("dossier"), dict) else {}
    metadata = audit_data.get("project_metadata", {}) if isinstance(audit_data.get("project_metadata"), dict) else {}
    crypto = dossier.get("crypto_verification", {}) if isinstance(dossier.get("crypto_verification"), dict) else {}
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    audit_type = "DEMO" if is_demo else "REAL"

    cursor.execute("""
        INSERT OR REPLACE INTO audits (
            dossier_id, project_name, scheme, contractor_name, tender_id,
            claim_amount, claimed_latitude, claimed_longitude, risk_score,
            verdict, decision_reason, recommended_action, sha256_seal,
            created_at_utc, raw_payload, audit_type, created_by, created_by_role, signature_block
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dossier.get("dossier_id", f"DOSSIER-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"),
        metadata.get("project_name", "Public Infrastructure Project"),
        metadata.get("scheme", "PMGSY"),
        metadata.get("contractor_name", "Unknown Contractor"),
        metadata.get("tender_id", "TDR-2024-001"),
        metadata.get("claim_amount", "₹0"),
        metadata.get("claimed_latitude", 0.0),
        metadata.get("claimed_longitude", 0.0),
        audit_data.get("risk_score", 0),
        audit_data.get("status", "CLEAR"),
        audit_data.get("decision_reason", "Pre-approval audit complete."),
        audit_data.get("recommended_action", "Proceed with disbursement."),
        crypto.get("sha256_seal", "UNAVAILABLE"),
        now_str,
        json.dumps(audit_data),
        audit_type,
        created_by,
        created_by_role,
        json.dumps(signature_block) if signature_block else None
    ))

    # Update Contractor Trust Score ONLY for non-demo live audits
    contractor_name = metadata.get("contractor_name")
    if contractor_name and not is_demo:
        is_flagged = 1 if audit_data.get("status") == "FLAGGED" else 0
        cursor.execute("SELECT * FROM contractors WHERE contractor_name = ?", (contractor_name,))
        existing = cursor.fetchone()

        if existing:
            new_violations = existing["past_violations"] + is_flagged
            new_score = max(10, existing["integrity_score"] - (20 if is_flagged else 0))
            new_stars = max(1.0, round((new_score / 100) * 5, 1))
            is_repeat = 1 if new_violations >= 2 else 0

            cursor.execute("""
                UPDATE contractors
                SET integrity_score = ?, star_rating = ?, past_violations = ?,
                    is_repeat_offender = ?, last_audited_at = ?
                WHERE contractor_name = ?
            """, (new_score, new_stars, new_violations, is_repeat, datetime.now(timezone.utc).isoformat(), contractor_name))

    conn.commit()
    conn.close()


def save_citizen_report(citizen_data: Dict[str, Any]):
    """Persists a citizen social audit report into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    cursor.execute("""
        INSERT OR REPLACE INTO citizen_reports (
            audit_id, project_id, project_name, citizen_notes, risk_score, verdict, created_at_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        citizen_data.get("audit_id", f"CIT-AUDIT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"),
        citizen_data.get("project_id", "PROJ-UNKNOWN"),
        citizen_data.get("project_name", "Public Work"),
        citizen_data.get("citizen_notes", ""),
        citizen_data.get("risk_score", 0),
        citizen_data.get("verdict", "CLEAR"),
        now_str
    ))

    conn.commit()
    conn.close()


def get_all_audits(limit: int = 50, audit_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves recent audit ledger entries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if audit_type:
        cursor.execute("SELECT * FROM audits WHERE audit_type = ? ORDER BY created_at_utc DESC LIMIT ?", (audit_type, limit))
    else:
        cursor.execute("SELECT * FROM audits ORDER BY created_at_utc DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_citizen_reports(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves recent citizen reports."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citizen_reports ORDER BY created_at_utc DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_db_analytics_summary() -> Dict[str, Any]:
    """Computes dynamic aggregate statistics from SQLite for the Macro Vigilance Cockpit."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN verdict='FLAGGED' THEN 1 ELSE 0 END) as flagged, SUM(CASE WHEN verdict='REVIEW' THEN 1 ELSE 0 END) as review, SUM(CASE WHEN verdict='CLEAR' THEN 1 ELSE 0 END) as clear FROM audits")
    stats = cursor.fetchone()

    cursor.execute("SELECT * FROM audits WHERE claimed_latitude != 0.0 AND claimed_longitude != 0.0 ORDER BY created_at_utc DESC LIMIT 20")
    geo_audits = cursor.fetchall()

    conn.close()
    return {
        "total_audits": stats["total"] if stats else 0,
        "flagged_count": stats["flagged"] if stats else 0,
        "review_count": stats["review"] if stats else 0,
        "clear_count": stats["clear"] if stats else 0,
        "geo_audits": [dict(r) for r in geo_audits]
    }


def get_audit_by_id(dossier_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single audit by Dossier ID for QR verification."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audits WHERE dossier_id = ?", (dossier_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
