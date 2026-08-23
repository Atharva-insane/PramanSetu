import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Find the backend folder where this file exists
BASE_DIR = Path(__file__).resolve().parent

# Explicitly load backend/.env
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


def analyze_genai_image(image_bytes, mime_type="image/jpeg"):

    """
    Sends the uploaded image to Gemini for a cautious
    visual forensic assessment.
    """

    # Read API key AFTER loading .env
    api_key = os.getenv("GEMINI_API_KEY")

    # Don't crash the backend if API key is missing
    if not api_key:
        return {
            "status": "UNVERIFIABLE",
            "is_suspicious": False,
            "confidence": 0.0,
            "reason": "GEMINI_API_KEY not found in backend/.env"
        }

    try:
        client = genai.Client(api_key=api_key)

        prompt = """
You are a visual forensic analysis assistant for CivicAudit AI.

Analyze this image for possible signs of:
- AI generation
- synthetic imagery
- image manipulation
- inconsistent lighting or shadows
- warped objects or geometry
- repeated visual patterns
- unnatural textures
- impossible reflections
- inconsistent perspective
- suspicious blending artifacts

IMPORTANT:
Do not claim with certainty that an image is AI-generated.
This is only a preliminary forensic assessment.

Return ONLY valid JSON.
Do not use markdown.
Do not add any explanation outside the JSON.

Use exactly this format:
{
    "status": "CLEAR" or "REVIEW",
    "is_suspicious": true or false,
    "confidence": 0.0,
    "reason": "Short explanation of the visual assessment"
}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_bytes
                            }
                        }
                    ]
                }
            ]
        )

        response_text = response.text.strip()

        # Remove markdown fences if returned accidentally
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        result = json.loads(response_text)

        return {
            "status": result.get("status", "REVIEW"),
            "is_suspicious": result.get("is_suspicious", False),
            "confidence": float(result.get("confidence", 0.0)),
            "reason": result.get("reason", "No reason provided")
        }

    except Exception as e:
        return {
            "status": "UNVERIFIABLE",
            "is_suspicious": False,
            "confidence": 0.0,
            "reason": f"Gemini analysis unavailable: {str(e)}"
        }