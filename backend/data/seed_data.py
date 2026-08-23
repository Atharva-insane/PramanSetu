import os
import struct
import io
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import piexif
import imagehash

DATA_DIR = Path(__file__).resolve().parent
SAMPLE_IMAGES_DIR = DATA_DIR / "sample_images"
SAMPLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def create_gps_exif(latitude: float, longitude: float, timestamp: str = "2024:07:15 14:00:00") -> bytes:
    """Encodes GPS coordinates into raw EXIF bytes."""
    def to_deg(value, loc):
        if value < 0:
            loc_value = loc[0]
        else:
            loc_value = loc[1]
        abs_value = abs(value)
        deg = int(abs_value)
        t1 = (abs_value - deg) * 60
        min = int(t1)
        sec = round((t1 - min) * 60, 4)
        return (
            ((deg, 1), (min, 1), (int(sec * 100), 100)),
            loc_value
        )

    lat_dms, lat_ref = to_deg(latitude, ["S", "N"])
    lng_dms, lng_ref = to_deg(longitude, ["W", "E"])

    zeroth_ifd = {
        piexif.ImageIFD.Make: "Nikon",
        piexif.ImageIFD.Model: "D7500 Engineering Survey Camera",
        piexif.ImageIFD.DateTime: timestamp
    }

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_ref,
        piexif.GPSIFD.GPSLatitude: lat_dms,
        piexif.GPSIFD.GPSLongitudeRef: lng_ref,
        piexif.GPSIFD.GPSLongitude: lng_dms,
    }

    exif_dict = {"0th": zeroth_ifd, "GPS": gps_ifd, "Exif": {}, "1st": {}, "thumbnail": None}
    return piexif.dump(exif_dict)


def generate_benchmark_assets():
    print(f"Generating deterministic test assets in: {SAMPLE_IMAGES_DIR}")

    # =========================================================================
    # DEMO 1: The Gold Standard Compliant Baseline (Clean Infrastructure Project)
    # PMGSY Bituminous Road, Varanasi (25.3176 N, 82.9739 E)
    # =========================================================================
    img1 = Image.new("RGB", (640, 480), color=(50, 60, 70))
    draw1 = ImageDraw.Draw(img1)
    # Draw finished road surface
    draw1.rectangle([0, 180, 640, 480], fill=(35, 38, 42))  # Dark asphalt
    draw1.line([(320, 220), (320, 480)], fill=(245, 245, 120), width=6)  # Road marking
    draw1.rectangle([0, 180, 640, 200], fill=(70, 75, 80))  # Curbing
    draw1.text((20, 20), "PMGSY RURAL ROAD - COMPLIANT BENCHMARK 2024", fill=(255, 255, 255))
    draw1.text((20, 45), "GPS: 25.3176 N, 82.9739 E | VARANASI SECTOR 4", fill=(200, 230, 200))
    
    exif1 = create_gps_exif(25.3176, 82.9739, "2024:07:15 11:30:00")
    demo1_path = SAMPLE_IMAGES_DIR / "demo1_clean_road.jpg"
    img1.save(demo1_path, "JPEG", exif=exif1, quality=92)
    hash1 = str(imagehash.phash(img1))
    print(f"[+] Created demo1_clean_road.jpg (Clean Project - pHash: {hash1})")

    # Demo 1 Clean Muster Roll (25 Verified Workers, zero duplicates/ghosts)
    clean_csv_path = SAMPLE_IMAGES_DIR / "demo1_clean_muster.csv"
    with open(clean_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["worker_id", "name", "trade", "days_worked", "daily_wage"])
        trades = ["Mason", "Helper", "Operator", "Helper", "Supervisor"]
        for i in range(1, 26):
            trade = trades[(i - 1) % len(trades)]
            wage = 550 if trade in ["Mason", "Supervisor"] else (700 if trade == "Operator" else 450)
            writer.writerow([f"W-10{i:02d}", f"Verified Worker {i}", trade, "26", str(wage)])
    print(f"[+] Created demo1_clean_muster.csv (25 Verified Workers)")


    # =========================================================================
    # DEMO 2: Multi-Vector Forensic Flag (Recycled Asset + Ghost Labor + Anomaly)
    # Jal Jeevan Mission Pipeline Claim
    # =========================================================================
    img2 = Image.new("RGB", (640, 480), color=(25, 75, 135))
    draw2 = ImageDraw.Draw(img2)
    # Draw pipeline
    draw2.rectangle([40, 140, 600, 360], fill=(65, 125, 175))
    draw2.rectangle([80, 180, 560, 320], fill=(30, 90, 150))
    draw2.text((20, 20), "JAL JEEVAN MISSION - PIPELINE ASSET VOUCHER", fill=(255, 255, 255))
    draw2.text((20, 45), "CLAIMED SITE: PRAYAGRAJ (ZONE-UP-001)", fill=(255, 200, 200))
    
    # Save base and compute hash
    demo2_path = SAMPLE_IMAGES_DIR / "demo2_fraud_pipeline.jpg"
    img2.save(demo2_path, "JPEG", quality=90)
    hash2 = str(imagehash.phash(img2))
    print(f"[+] Created demo2_fraud_pipeline.jpg (Duplicate Asset - pHash: {hash2})")

    # Demo 2 Fraud Muster Roll with 31 workers (2 Ghost IDs, 1 duplicate ID, 1 breach)
    fraud_csv_path = SAMPLE_IMAGES_DIR / "demo2_ghost_muster.csv"
    with open(fraud_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["worker_id", "name", "trade", "days_worked", "daily_wage"])
        writer.writerow(["W-2001", "Ramesh Kumar", "Mason", "26", "550"])
        writer.writerow(["W-2002", "Suresh Yadav", "Helper", "26", "450"])
        writer.writerow(["W-2003", "Dinesh Verma", "Helper", "26", "450"])
        writer.writerow(["W-2004", "GHOST-901", "Phantom Worker", "26", "500"])  # Ghost ID
        writer.writerow(["W-2005", "GHOST-902", "Phantom Worker", "26", "500"])  # Ghost ID
        writer.writerow(["W-2001", "Ramesh Kumar", "Mason", "26", "550"])       # Duplicate ID
        writer.writerow(["W-2006", "Mahesh Chand", "Operator", "45", "700"])     # Over 31 days breach
        for i in range(7, 32):
            writer.writerow([f"W-20{i:02d}", f"Laborer {i}", "Helper", "26", "450"])
    print(f"[+] Created demo2_ghost_muster.csv (Ghost Wages & Muster Leakage)")

    # Also keep backward compatibility aliases if needed
    img1.save(SAMPLE_IMAGES_DIR / "case1_clean_road.jpg", "JPEG", exif=exif1, quality=90)
    img2.save(SAMPLE_IMAGES_DIR / "case2_duplicate_pipeline.jpg", "JPEG", quality=90)

    print("\nDeterministic benchmark test assets generated successfully!")
    return hash1, hash2


if __name__ == "__main__":
    generate_benchmark_assets()
