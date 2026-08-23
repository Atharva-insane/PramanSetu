import sys
from pathlib import Path
from PIL import Image
import io
import imagehash

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.phash_service import check_asset_recycling, compute_image_phash
from schemas import SignalStatusEnum


def test_phash_exact_match():
    # Load case2_duplicate_pipeline.jpg which matches ASSET-UP-2023-001
    sample_path = BACKEND_DIR / "data" / "sample_images" / "case2_duplicate_pipeline.jpg"
    with open(sample_path, "rb") as f:
        image_bytes = f.read()

    result = check_asset_recycling(image_bytes)
    assert result.match_found is True
    assert result.status == SignalStatusEnum.FLAGGED
    assert result.hamming_distance is not None
    assert result.hamming_distance <= 5
    assert result.closest_match["asset_id"] == "ASSET-UP-2023-001"


def test_phash_unique_image():
    # Create a completely random noise image
    img = Image.new("RGB", (200, 200), color=(12, 199, 44))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    result = check_asset_recycling(image_bytes)
    assert result.match_found is False
    assert result.status == SignalStatusEnum.PASS
    assert result.hamming_distance is not None
    assert result.hamming_distance > 10
