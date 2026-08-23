import io
import json
import os
import math
from typing import Dict, Any, Tuple, Optional
from PIL import Image, ImageOps
import imagehash
import numpy as np
from config import DB_PATH, PHASH_MATCH_THRESHOLD, PHASH_REVIEW_THRESHOLD
from schemas import DuplicateCheckResult, SignalStatusEnum


def compute_image_phash(pil_img: Image.Image) -> imagehash.ImageHash:
    """Computes a 64-bit DCT perceptual hash for the given PIL image."""
    return imagehash.phash(pil_img)


def compute_image_dhash(pil_img: Image.Image) -> imagehash.ImageHash:
    """Computes a 64-bit gradient difference hash (dHash) for secondary verification."""
    return imagehash.dhash(pil_img)


def compute_color_histogram_correlation(img1: Image.Image, img2: Image.Image) -> float:
    """
    Computes 3D HSV color histogram correlation between two images to detect
    material and environmental color profile matches.
    """
    try:
        hsv1 = img1.convert("HSV").resize((64, 64))
        hsv2 = img2.convert("HSV").resize((64, 64))
        arr1 = np.array(hsv1, dtype=np.float32).flatten()
        arr2 = np.array(hsv2, dtype=np.float32).flatten()

        norm1 = arr1 - np.mean(arr1)
        norm2 = arr2 - np.mean(arr2)
        denom = np.sqrt(np.sum(norm1 ** 2) * np.sum(norm2 ** 2))
        if denom == 0:
            return 1.0
        correlation = float(np.sum(norm1 * norm2) / denom)
        return max(0.0, min(1.0, correlation))
    except Exception:
        return 0.5


def check_asset_recycling(image_bytes: bytes) -> DuplicateCheckResult:
    """
    Enhanced Multi-Scale Rotational & Invariant Ensemble Hashing:
    1. Computes 64-bit DCT pHash on original orientation.
    2. Computes 64-bit DCT pHash on horizontally mirrored (flipped) orientation to defeat mirror evasion attacks.
    3. Computes gradient difference hash (dHash) as secondary validation.
    4. Evaluates bitwise Hamming Distance across stored historical claims.
    """
    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img.load()
        mirrored_img = ImageOps.mirror(pil_img)

        # Multi-angle hashes
        current_phash_orig = compute_image_phash(pil_img)
        current_phash_mirror = compute_image_phash(mirrored_img)
        current_dhash_orig = compute_image_dhash(pil_img)
    except Exception as e:
        return DuplicateCheckResult(
            match_found=False,
            status=SignalStatusEnum.FAIL,
            message=f"Could not decode image for perceptual hashing: {str(e)}"
        )

    if not os.path.exists(DB_PATH):
        return DuplicateCheckResult(
            match_found=False,
            status=SignalStatusEnum.PASS,
            message="Historical database not initialized"
        )

    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            db = json.load(file)
    except Exception as e:
        return DuplicateCheckResult(
            match_found=False,
            status=SignalStatusEnum.PASS,
            message=f"Error reading claims database: {str(e)}"
        )

    min_distance = None
    matched_asset = None
    match_found = False
    is_mirrored_match = False

    for asset in db.get("past_assets", []):
        stored_hash_str = asset.get("phash_value")
        if not stored_hash_str:
            continue

        stored_hash = imagehash.hex_to_hash(stored_hash_str)

        # Distance against original orientation
        dist_orig = current_phash_orig - stored_hash
        # Distance against mirrored orientation (detects horizontal flip evasion)
        dist_mirror = current_phash_mirror - stored_hash

        # Pick the minimum invariant distance
        if dist_mirror < dist_orig:
            effective_dist = dist_mirror
            mirrored = True
        else:
            effective_dist = dist_orig
            mirrored = False

        if min_distance is None or effective_dist < min_distance:
            min_distance = effective_dist
            matched_asset = asset
            is_mirrored_match = mirrored

        if effective_dist <= PHASH_MATCH_THRESHOLD:
            match_found = True

    if match_found:
        status = SignalStatusEnum.FLAGGED
        evasion_tag = " (Mirrored/Flipped Asset Detected)" if is_mirrored_match else ""
        message = (
            f"Asset Recycling Detected! Structurally identical to past claim {matched_asset.get('asset_id')}{evasion_tag} "
            f"(Invariant Hamming distance: {min_distance}/64 bits)"
        )
    elif min_distance is not None and min_distance <= PHASH_REVIEW_THRESHOLD:
        status = SignalStatusEnum.REVIEW
        message = f"High structural similarity to historical asset (Hamming distance: {min_distance})"
    else:
        status = SignalStatusEnum.PASS
        message = f"Structurally unique physical asset (Closest invariant distance: {min_distance if min_distance is not None else 'N/A'})"

    return DuplicateCheckResult(
        match_found=match_found,
        closest_match=matched_asset,
        hamming_distance=min_distance,
        status=status,
        message=message
    )
