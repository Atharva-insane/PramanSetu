import io
import math
from typing import Optional, Tuple, Dict, Any
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from config import LOCATION_MATCH_TOLERANCE_METRES, LOCATION_REVIEW_TOLERANCE_METRES
from schemas import GPSExtractionResult, LocationCheckResult, SignalStatusEnum


def _convert_to_degrees(value) -> Optional[float]:
    """Helper function to convert EXIF GPS coordinates (degrees, minutes, seconds) to decimal degrees."""
    try:
        if isinstance(value, tuple) and len(value) == 3:
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)
        return float(value)
    except Exception:
        return None


def extract_gps_metadata(image_bytes: bytes) -> GPSExtractionResult:
    """Extracts raw hardware EXIF GPS tags and camera metadata from image bytes."""
    try:
        tags = exifread.process_file(io.BytesIO(image_bytes), details=False)
        
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
        timestamp = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
        camera_make = tags.get('Image Make')
        camera_model = tags.get('Image Model')

        lat = None
        lon = None

        if gps_latitude and gps_latitude_ref:
            lat_values = [float(x.num) / float(x.den) for x in gps_latitude.values]
            lat = lat_values[0] + (lat_values[1] / 60.0) + (lat_values[2] / 3600.0)
            if str(gps_latitude_ref) in ['S', 's']:
                lat = -lat

        if gps_longitude and gps_longitude_ref:
            lon_values = [float(x.num) / float(x.den) for x in gps_longitude.values]
            lon = lon_values[0] + (lon_values[1] / 60.0) + (lon_values[2] / 3600.0)
            if str(gps_longitude_ref) in ['W', 'w']:
                lon = -lon

        # Fallback to PIL EXIF
        if lat is None or lon is None:
            pil_img = Image.open(io.BytesIO(image_bytes))
            exif = pil_img._getexif()
            if exif:
                gps_info = {}
                for tag_id, val in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "GPSInfo":
                        for key in val:
                            sub_tag = GPSTAGS.get(key, key)
                            gps_info[sub_tag] = val[key]
                
                if "GPSLatitude" in gps_info and "GPSLatitudeRef" in gps_info:
                    lat_deg = _convert_to_degrees(gps_info["GPSLatitude"])
                    if lat_deg is not None:
                        lat = -lat_deg if gps_info["GPSLatitudeRef"] in ["S", "s"] else lat_deg

                if "GPSLongitude" in gps_info and "GPSLongitudeRef" in gps_info:
                    lon_deg = _convert_to_degrees(gps_info["GPSLongitude"])
                    if lon_deg is not None:
                        lon = -lon_deg if gps_info["GPSLongitudeRef"] in ["W", "w"] else lon_deg

                if not timestamp and "DateTimeOriginal" in exif:
                    timestamp = exif["DateTimeOriginal"]
                if not camera_make and "Make" in exif:
                    camera_make = exif["Make"]
                if not camera_model and "Model" in exif:
                    camera_model = exif["Model"]

        gps_found = (lat is not None and lon is not None)
        return GPSExtractionResult(
            gps_found=gps_found,
            latitude=round(lat, 6) if lat is not None else None,
            longitude=round(lon, 6) if lon is not None else None,
            timestamp=str(timestamp) if timestamp else None,
            device_make=str(camera_make) if camera_make else None,
            device_model=str(camera_model) if camera_model else None
        )

    except Exception as e:
        return GPSExtractionResult(
            gps_found=False,
            latitude=None,
            longitude=None,
            timestamp=None,
            device_make=None,
            device_model=None
        )


def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates spherical great-circle distance between two GPS coordinates in metres."""
    R = 6371000.0  # Earth radius in metres
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def calculate_vincenty_ellipsoidal_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates precise geodesic distance between two points on the WGS-84 Reference Ellipsoid
    using Vincenty's Inverse Geodetic Formula (accurate to 0.5 millimeters).
    """
    a = 6378137.0          # Major axis in metres
    f = 1.0 / 298.257223563 # Flattening
    b = (1.0 - f) * a      # Minor axis: 6356752.314245 m

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    L = math.radians(lon2 - lon1)

    U1 = math.atan((1.0 - f) * math.tan(phi1))
    U2 = math.atan((1.0 - f) * math.tan(phi2))
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    lamb = L
    lamb_prev = 2.0 * math.pi
    iterations = 0
    max_iterations = 200

    sin_sigma = 0.0
    cos_sigma = 0.0
    sigma = 0.0
    sin_alpha = 0.0
    cos2_alpha = 0.0
    cos2_sigma_m = 0.0

    while abs(lamb - lamb_prev) > 1e-12 and iterations < max_iterations:
        iterations += 1
        sin_lamb = math.sin(lamb)
        cos_lamb = math.cos(lamb)

        sin_sigma = math.sqrt((cosU2 * sin_lamb) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cos_lamb) ** 2)
        if sin_sigma == 0:
            return 0.0

        cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cos_lamb
        sigma = math.atan2(sin_sigma, cos_sigma)

        sin_alpha = (cosU1 * cosU2 * sin_lamb) / sin_sigma
        cos2_alpha = 1.0 - sin_alpha ** 2

        if cos2_alpha == 0:
            cos2_sigma_m = 0.0
        else:
            cos2_sigma_m = cos_sigma - (2.0 * sinU1 * sinU2 / cos2_alpha)

        C = (f / 16.0) * cos2_alpha * (4.0 + f * (4.0 - 3.0 * cos2_alpha))
        lamb_prev = lamb
        lamb = L + (1.0 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1.0 + 2.0 * cos2_sigma_m ** 2))
        )

    if iterations >= max_iterations:
        return calculate_haversine_distance(lat1, lon1, lat2, lon2)

    u2 = cos2_alpha * ((a ** 2 - b ** 2) / (b ** 2))
    A = 1.0 + (u2 / 16384.0) * (4096.0 + u2 * (-768.0 + u2 * (320.0 - 175.0 * u2)))
    B = (u2 / 1024.0) * (256.0 + u2 * (-128.0 + u2 * (74.0 - 47.0 * u2)))

    delta_sigma = B * sin_sigma * (
        cos2_sigma_m + (B / 4.0) * (
            cos_sigma * (-1.0 + 2.0 * cos2_sigma_m ** 2) -
            (B / 6.0) * cos2_sigma_m * (-3.0 + 4.0 * sin_sigma ** 2) * (-3.0 + 4.0 * cos2_sigma_m ** 2)
        )
    )

    s = b * A * (sigma - delta_sigma)
    return s


def verify_location_geodesic(
    gps_result: GPSExtractionResult,
    claimed_lat: float,
    claimed_lon: float
) -> LocationCheckResult:
    """
    Verifies on-site EXIF coordinates against claimed tender coordinates
    using the precision WGS-84 Vincenty Ellipsoidal Geodesic Model.
    """
    if not gps_result.gps_found or gps_result.latitude is None or gps_result.longitude is None:
        return LocationCheckResult(
            photo_gps_found=False,
            claimed_latitude=claimed_lat,
            claimed_longitude=claimed_lon,
            photo_latitude=None,
            photo_longitude=None,
            distance_metres=None,
            location_match=False,
            status=SignalStatusEnum.UNVERIFIABLE,
            message="No embedded hardware GPS EXIF metadata found in submitted evidence image."
        )

    # Compute high-precision WGS-84 ellipsoidal distance
    distance = calculate_vincenty_ellipsoidal_distance(
        gps_result.latitude,
        gps_result.longitude,
        claimed_lat,
        claimed_lon
    )
    distance_rounded = round(distance, 1)

    if distance <= LOCATION_MATCH_TOLERANCE_METRES:
        status = SignalStatusEnum.MATCH
        location_match = True
        message = (
            f"Geodesic Location Verified (WGS-84 Ellipsoid): Evidence captured within "
            f"{distance_rounded}m of claimed project site (Tolerance: {LOCATION_MATCH_TOLERANCE_METRES}m)."
        )
    elif distance <= LOCATION_REVIEW_TOLERANCE_METRES:
        status = SignalStatusEnum.REVIEW
        location_match = False
        message = (
            f"Boundary Warning: Evidence captured {distance_rounded}m from claimed project coordinates "
            f"(Permissible corridor: {LOCATION_REVIEW_TOLERANCE_METRES}m)."
        )
    else:
        status = SignalStatusEnum.MISMATCH
        location_match = False
        distance_km = round(distance / 1000.0, 2)
        message = (
            f"Severe Location Fraud Detected: Photo was physically captured {distance_km} km away "
            f"from the sanctioned project site (Claimed: {claimed_lat}, {claimed_lon} | Actual: {gps_result.latitude}, {gps_result.longitude})."
        )

    return LocationCheckResult(
        photo_gps_found=True,
        claimed_latitude=claimed_lat,
        claimed_longitude=claimed_lon,
        photo_latitude=gps_result.latitude,
        photo_longitude=gps_result.longitude,
        distance_metres=distance_rounded,
        location_match=location_match,
        status=status,
        message=message
    )
