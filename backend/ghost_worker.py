import cv2
import numpy as np
from PIL import Image
import io


def analyze_workers(image_bytes):
    """
    Runs lightweight forensic workers in parallel-style modules.
    Currently checks:
    1. Face detection
    2. Image dimensions
    3. Basic image integrity
    """

    results = {}

    # ==========================================
    # WORKER 1: IMAGE DECODE + DIMENSION CHECK
    # ==========================================

    try:
        img = Image.open(io.BytesIO(image_bytes))

        width, height = img.size

        results["image_analysis"] = {
            "status": "PASS",
            "width": width,
            "height": height,
            "format": img.format,
            "message": "Image decoded successfully"
        }

    except Exception as e:
        results["image_analysis"] = {
            "status": "FAIL",
            "message": f"Could not decode image: {str(e)}"
        }

        return results

    # ==========================================
    # WORKER 2: FACE DETECTION
    # ==========================================

    try:
        image_array = np.frombuffer(image_bytes, np.uint8)

        cv_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if cv_image is None:
            raise Exception("OpenCV could not decode image")

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        face_count = len(faces)

        results["face_detection"] = {
            "status": "REVIEW" if face_count > 0 else "PASS",
            "faces_detected": face_count,
            "message": (
                f"{face_count} face(s) detected"
                if face_count > 0
                else "No faces detected"
            )
        }

    except Exception as e:
        results["face_detection"] = {
            "status": "UNVERIFIABLE",
            "faces_detected": 0,
            "message": f"Face analysis failed: {str(e)}"
        }

    # ==========================================
    # WORKER 3: IMAGE SIZE / QUALITY CHECK
    # ==========================================

    try:
        image_size_bytes = len(image_bytes)

        if image_size_bytes < 5 * 1024:
            quality_status = "REVIEW"
            quality_message = "Image file is unusually small"
        else:
            quality_status = "PASS"
            quality_message = "Image file size appears normal"

        results["quality_check"] = {
            "status": quality_status,
            "file_size_bytes": image_size_bytes,
            "message": quality_message
        }

    except Exception as e:
        results["quality_check"] = {
            "status": "UNVERIFIABLE",
            "message": str(e)
        }

    return results