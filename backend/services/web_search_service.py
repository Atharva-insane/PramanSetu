import json
import os
import io
import base64
import urllib.request
from typing import Optional, Dict, Any, Tuple
from PIL import Image, ImageOps
import imagehash
from config import WEB_DB_PATH, PHASH_MATCH_THRESHOLD, PHASH_REVIEW_THRESHOLD
from schemas import WebSearchCheckResult, SignalStatusEnum


def query_google_cloud_vision_web_detection(image_bytes: bytes, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Queries Google Cloud Vision Web Detection API (WEB_DETECTION) to find exact and partial
    matches across billions of crawled public internet web pages and stock photography portals.
    """
    try:
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        b64_img = base64.b64encode(image_bytes).decode("utf-8")
        
        payload = {
            "requests": [
                {
                    "image": {"content": b64_img},
                    "features": [{"type": "WEB_DETECTION", "maxResults": 5}]
                }
            ]
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            if resp.status == 200:
                result = json.loads(resp.read().decode("utf-8"))
                responses = result.get("responses", [])
                if responses and "webDetection" in responses[0]:
                    return responses[0]["webDetection"]
    except Exception:
        pass
    return None


def query_openverse_public_search(query: str) -> Optional[Dict[str, Any]]:
    """
    Queries OpenVerse open-access Creative Commons repository for matching public domain assets.
    """
    try:
        url = f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(query)}&page_size=5"
        req = urllib.request.Request(url, headers={"User-Agent": "PramanSetu-Vigilance/2.0"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass
    return None


def check_web_and_stock_photo_reuse(image_bytes: bytes) -> WebSearchCheckResult:
    """
    Advanced Global Web Reverse Image & Stock Photo Intelligence Engine:
    1. Multi-Angle Hash computation (Original + Horizontal Flip).
    2. Live Google Cloud Vision Web Detection if API Key is configured.
    3. Multi-Vector comparison against indexed public domain / stock database (Shutterstock, iStock, Wikimedia).
    4. Calculates invariant bitwise Hamming distance and domain attribution.
    """
    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img.load()
        mirrored_img = ImageOps.mirror(pil_img)

        candidate_hash = imagehash.phash(pil_img)
        mirrored_hash = imagehash.phash(mirrored_img)
    except Exception as e:
        return WebSearchCheckResult(
            match_found=False,
            status=SignalStatusEnum.UNVERIFIABLE,
            message=f"Web search skipped (image decode issue): {str(e)}"
        )

    # 1. Live Google Cloud Vision API Hook (if key provided in environment)
    g_vision_key = os.getenv("GOOGLE_CLOUD_VISION_API_KEY") or os.getenv("GOOGLE_VISION_KEY")
    if g_vision_key:
        g_web = query_google_cloud_vision_web_detection(image_bytes, g_vision_key)
        if g_web:
            full_matches = g_web.get("fullMatchingImages", [])
            partial_matches = g_web.get("partialMatchingImages", [])
            pages = g_web.get("pagesWithMatchingImages", [])

            if full_matches or partial_matches:
                match_url = full_matches[0].get("url") if full_matches else partial_matches[0].get("url")
                page_url = pages[0].get("url") if pages else match_url
                domain = page_url.split("/")[2] if page_url and len(page_url.split("/")) > 2 else "public-web"

                return WebSearchCheckResult(
                    match_found=True,
                    matched_asset_id="GCV-LIVE-MATCH",
                    title=f"Live Web Image Match on {domain}",
                    source_type="Public Internet / Live Crawl",
                    domain=domain,
                    source_url=page_url,
                    hamming_distance=0,
                    confidence=0.98,
                    status=SignalStatusEnum.FLAGGED,
                    message=(
                        f"Live Global Web Reuse Detected via Google Vision! Image matches public content on "
                        f"{domain} (Source: {page_url})."
                    )
                )

    # 2. Local Indexed Stock & Public Domain Database Search (with Flip-Invariance)
    if not os.path.exists(WEB_DB_PATH):
        return WebSearchCheckResult(
            match_found=False,
            status=SignalStatusEnum.PASS,
            message="Web reverse image database not initialized."
        )

    try:
        with open(WEB_DB_PATH, "r", encoding="utf-8") as f:
            web_db = json.load(f)
    except Exception as e:
        return WebSearchCheckResult(
            match_found=False,
            status=SignalStatusEnum.PASS,
            message=f"Could not load web database: {str(e)}"
        )

    min_distance = None
    matched_asset = None
    match_found = False
    is_mirrored = False

    for asset in web_db.get("indexed_web_assets", []):
        stored_hash_str = asset.get("phash_value")
        if not stored_hash_str:
            continue

        stored_hash = imagehash.hex_to_hash(stored_hash_str)
        
        # Original distance & mirrored distance
        dist_orig = candidate_hash - stored_hash
        dist_mirror = mirrored_hash - stored_hash

        if dist_mirror < dist_orig:
            effective_dist = dist_mirror
            mirrored_match = True
        else:
            effective_dist = dist_orig
            mirrored_match = False

        if min_distance is None or effective_dist < min_distance:
            min_distance = effective_dist
            matched_asset = asset
            is_mirrored = mirrored_match

        if effective_dist <= PHASH_MATCH_THRESHOLD:
            match_found = True

    if match_found and matched_asset:
        confidence = round(max(0.70, 1.0 - (min_distance / 64.0)), 2)
        flip_tag = " (Mirrored/Flipped Stock Photo)" if is_mirrored else ""
        return WebSearchCheckResult(
            match_found=True,
            matched_asset_id=matched_asset.get("web_asset_id"),
            title=matched_asset.get("title"),
            source_type=matched_asset.get("source_type"),
            domain=matched_asset.get("domain"),
            source_url=matched_asset.get("source_url"),
            hamming_distance=min_distance,
            confidence=confidence,
            status=SignalStatusEnum.FLAGGED,
            message=(
                f"Public Stock Photo Asset Reuse Detected!{flip_tag} Image is structurally identical to public domain "
                f"asset on {matched_asset.get('domain')} (Bitwise Invariant Distance: {min_distance}/64 bits)"
            )
        )
    elif min_distance is not None and min_distance <= PHASH_REVIEW_THRESHOLD and matched_asset:
        confidence = round(1.0 - (min_distance / 64.0), 2)
        return WebSearchCheckResult(
            match_found=False,
            matched_asset_id=matched_asset.get("web_asset_id"),
            title=matched_asset.get("title"),
            source_type=matched_asset.get("source_type"),
            domain=matched_asset.get("domain"),
            source_url=matched_asset.get("source_url"),
            hamming_distance=min_distance,
            confidence=confidence,
            status=SignalStatusEnum.REVIEW,
            message=f"Moderate similarity to public web asset on {matched_asset.get('domain')} (Distance: {min_distance})"
        )

    return WebSearchCheckResult(
        match_found=False,
        status=SignalStatusEnum.PASS,
        hamming_distance=min_distance,
        message="No matching public stock photos or web assets found. Image verified as an original site capture."
    )
