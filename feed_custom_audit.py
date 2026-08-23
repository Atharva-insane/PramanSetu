#!/usr/bin/env python3
"""
PramanSetu — Direct Custom Audit Ingestion Script
Use this script to feed custom audit claims, images, and muster rolls directly
to the running PramanSetu backend API.

Usage:
  python feed_custom_audit.py --image path/to/photo.jpg --project "My Rural Road" --contractor "My Builder Ltd" --claim "₹25,00,000" --lat 25.3176 --lon 82.9739
"""

import os
import sys
import argparse
import json
import urllib.request
import urllib.parse
import mimetypes
import uuid


def submit_audit_via_multipart(
    api_url: str,
    image_path: str,
    project_name: str,
    scheme: str,
    contractor_name: str,
    tender_id: str,
    claim_amount: str,
    claimed_lat: float,
    claimed_lon: float,
    claimed_material: str,
    claimed_timestamp: str,
    muster_csv_path: str = None
):
    if not os.path.exists(image_path):
        print(f"Error: Photographic proof file not found: {image_path}")
        return

    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    body = bytearray()

    fields = {
        "project_name": project_name,
        "scheme": scheme,
        "contractor_name": contractor_name,
        "tender_id": tender_id,
        "claim_amount": claim_amount,
        "claimed_latitude": str(claimed_lat),
        "claimed_longitude": str(claimed_lon),
        "claimed_material": claimed_material,
        "claimed_timestamp": claimed_timestamp,
        "is_demo": "false"
    }

    # Add text form fields
    for field_name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    # Add image file
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    img_filename = os.path.basename(image_path)
    mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="image"; filename="{img_filename}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(img_bytes)
    body.extend(b"\r\n")

    # Add optional muster roll CSV
    if muster_csv_path and os.path.exists(muster_csv_path):
        with open(muster_csv_path, "rb") as mf:
            csv_bytes = mf.read()
        csv_filename = os.path.basename(muster_csv_path)
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="muster_roll_csv"; filename="{csv_filename}"\r\n'.encode("utf-8"))
        body.extend(b"Content-Type: text/csv\r\n\r\n")
        body.extend(csv_bytes)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    print(f"Submitting audit to: {api_url}/api/audit/milestone")
    print(f"   Project: {project_name}")
    print(f"   Contractor: {contractor_name}")
    print(f"   Claim Amount: {claim_amount}")
    print(f"   Claimed GPS: {claimed_lat}, {claimed_lon}")

    req = urllib.request.Request(
        f"{api_url}/api/audit/milestone",
        data=bytes(body),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
            "User-Agent": "PramanSetu-CLI-Feeder/2.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            print("\n" + "=" * 60)
            print("FORENSIC AUDIT COMPLETED")
            print("=" * 60)
            print(f"Verdict        : {resp_data.get('status')}")
            print(f"Risk Score     : {resp_data.get('risk_score')}/100")
            print(f"Decision Reason: {resp_data.get('decision_reason')}")
            print(f"Action         : {resp_data.get('recommended_action')}")
            dossier = resp_data.get("dossier", {})
            print(f"Dossier ID     : {dossier.get('dossier_id')}")
            crypto = dossier.get("crypto_verification", {})
            print(f"SHA-256 Seal   : {crypto.get('sha256_seal', 'N/A')[:32]}...")
            print("=" * 60)
            print(f"View live in UI at: http://localhost:3000/dashboard")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        print("Ensure the backend server is running on http://localhost:8000")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Feed custom audit data to PramanSetu")
    parser.add_argument("--image", required=True, help="Path to evidence JPEG/PNG photo")
    parser.add_argument("--project", default="Custom Public Work Milestone", help="Project name")
    parser.add_argument("--scheme", default="Pradhan Mantri Gram Sadak Yojana (PMGSY)", help="Scheme name")
    parser.add_argument("--contractor", default="Apex Buildcon Pvt. Ltd.", help="Contractor name")
    parser.add_argument("--tender", default="TDR-2024-CUSTOM-001", help="Tender ID")
    parser.add_argument("--claim", default="₹35,00,000", help="Claimed amount")
    parser.add_argument("--lat", type=float, default=25.3176, help="Claimed Latitude")
    parser.add_argument("--lon", type=float, default=82.9739, help="Claimed Longitude")
    parser.add_argument("--material", default="Finished Bituminous Asphalt", help="Claimed material")
    parser.add_argument("--timestamp", default="2024-07-15 14:00", help="Claimed date/time")
    parser.add_argument("--muster", help="Optional path to muster roll CSV")
    parser.add_argument("--url", default="http://localhost:8000", help="Backend API base URL")

    args = parser.parse_args()
    submit_audit_via_multipart(
        api_url=args.url,
        image_path=args.image,
        project_name=args.project,
        scheme=args.scheme,
        contractor_name=args.contractor,
        tender_id=args.tender,
        claim_amount=args.claim,
        claimed_lat=args.lat,
        claimed_lon=args.lon,
        claimed_material=args.material,
        claimed_timestamp=args.timestamp,
        muster_csv_path=args.muster
    )
