import sys
from pathlib import Path
from PIL import Image
import io

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.web_search_service import check_web_and_stock_photo_reuse
from schemas import SignalStatusEnum


def test_web_search_stock_photo_hit():
    sample_path = BACKEND_DIR / "data" / "sample_images" / "case4_web_stock_photo.jpg"
    with open(sample_path, "rb") as f:
        image_bytes = f.read()

    result = check_web_and_stock_photo_reuse(image_bytes)
    assert result.match_found is True
    assert result.status == SignalStatusEnum.FLAGGED
    assert result.domain == "shutterstock.com"
    assert result.matched_asset_id == "WEB-STOCK-001"
    assert result.confidence >= 0.70


def test_web_search_original_capture():
    img = Image.new("RGB", (200, 200), color=(140, 20, 85))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    result = check_web_and_stock_photo_reuse(image_bytes)
    assert result.match_found is False
    assert result.status == SignalStatusEnum.PASS
