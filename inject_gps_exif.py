#!/usr/bin/env python3
"""
PramanSetu — GPS EXIF Hardware Telemetry Stamping Tool
Use this utility to embed authentic GPS coordinates and camera metadata into any JPEG image
to test geotagged milestone verification.

Usage Example:
  python inject_gps_exif.py --image my_site_photo.jpg --lat 25.3176 --lon 82.9739 --output tagged_photo.jpg
"""

import os
import sys
import argparse
from datetime import datetime

try:
    from PIL import Image
    import piexif
except ImportError:
    print("Error: Required packages 'pillow' and 'piexif' are not installed.")
    print("Install with: pip install pillow piexif")
    sys.exit(1)


def to_deg(value, loc):
    """Converts decimal degrees to EXIF rational tuple format."""
    if value < 0:
        loc_value = loc[0]
    else:
        loc_value = loc[1]
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min_val = int(t1)
    sec_val = round((t1 - min_val) * 60, 4)
    return (
        ((deg, 1), (min_val, 1), (int(sec_val * 100), 100)),
        loc_value
    )


def inject_gps(image_path: str, latitude: float, longitude: float, output_path: str = None, timestamp: str = None):
    if not os.path.exists(image_path):
        print(f"Error: Input image not found: {image_path}")
        return False

    if not output_path:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_geotagged{ext}"

    if not timestamp:
        timestamp = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

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
    exif_bytes = piexif.dump(exif_dict)

    img = Image.open(image_path)
    img.save(output_path, "JPEG", exif=exif_bytes, quality=95)

    print(f"Successfully stamped GPS telemetry into: {output_path}")
    print(f"   Latitude : {latitude} ({lat_ref})")
    print(f"   Longitude: {longitude} ({lng_ref})")
    print(f"   Timestamp: {timestamp}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PramanSetu GPS EXIF Stamping Tool")
    parser.add_argument("--image", required=True, help="Path to input JPEG image")
    parser.add_argument("--lat", type=float, default=25.3176, help="Target Latitude (default: 25.3176 - Varanasi)")
    parser.add_argument("--lon", type=float, default=82.9739, help="Target Longitude (default: 82.9739 - Varanasi)")
    parser.add_argument("--output", help="Optional output path for tagged image")
    parser.add_argument("--timestamp", help="Optional timestamp (format: YYYY:MM:DD HH:MM:SS)")

    args = parser.parse_args()
    inject_gps(args.image, args.lat, args.lon, args.output, args.timestamp)
