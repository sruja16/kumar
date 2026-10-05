import os
import json

import numpy as np
from PIL import Image
from ultralytics import YOLO

from google import genai
from google.genai import types


# ============================================================
# CONFIGURATION
# ============================================================

WEIGHTS_PATH = "best.pt"

# Read Gemini API key from environment variable.
# DO NOT put the API key directly in this file.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set.\n"
        "Set it in your terminal before running Streamlit."
    )


# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

try:
    _model = YOLO(WEIGHTS_PATH)
    _model.to("cpu")
except Exception as e:
    raise RuntimeError(
        f"Could not load YOLO model from '{WEIGHTS_PATH}': {e}"
    )


# ============================================================
# PEST DETECTION
# ============================================================

def detect_pest(image: Image.Image, imgsz: int = 640):
    """
    Run YOLOv8 inference on a PIL image.

    Returns:
        frame     -> annotated image
        pest_name -> highest-confidence detected pest
    """

    # Convert PIL image to RGB NumPy array
    image_np = np.array(image.convert("RGB"))

    # Run YOLO inference
    results = _model.predict(
        source=image_np,
        imgsz=imgsz,
        device="cpu",
        verbose=False
    )

    result = results[0]

    # Create annotated image
    frame = result.plot()

    # Get detected boxes
    boxes = result.boxes

    # No pest detected
    if boxes is None or len(boxes) == 0:
        return frame, None

    # Confidence values
    confs = boxes.conf.cpu().numpy()

    # Class IDs
    classes = boxes.cls.cpu().numpy().astype(int)

    # Select highest-confidence detection
    best_idx = int(confs.argmax())

    class_id = int(classes[best_idx])

    # Get pest name
    pest_name = result.names[class_id]

    return frame, pest_name


# ============================================================
# GEMINI CROP PROTECTION ADVICE
# ============================================================

def get_advice(pest_name: str) -> dict:
    """
    Get crop protection advice from Gemini.

    Returns a dictionary containing:
        pest
        common_name_en
        common_name_hi
        chemical
        organic
        prevention
        crop_stage
    """

    prompt = f"""
You are an expert agricultural pest and crop protection advisor.

The computer vision model detected this pest:

{pest_name}

Identify the pest and provide practical crop protection information.

Return ONLY a JSON object.

The JSON must contain exactly these fields:

- pest:
  Scientific name of the pest.

- common_name_en:
  Common English name.

- common_name_hi:
  Common Hindi name written in Devanagari.

- chemical:
  A suitable chemical control option.
  Mention active ingredient, approximate application guidance,
  and method where appropriate.
  Advise following the product label and local agricultural guidance.

- organic:
  An organic or natural control method.
  Give concise preparation/application instructions.

- prevention:
  Practical prevention methods for farmers.

- crop_stage:
  Crop growth stage when this pest commonly causes damage.

Keep every value concise and useful.

Do not return Markdown.
Do not return ```json.
Do not add explanations outside the JSON object.
"""


    try:

        # ====================================================
        # Gemini structured JSON response
        # ====================================================

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "pest": {
                            "type": "STRING"
                        },
                        "common_name_en": {
                            "type": "STRING"
                        },
                        "common_name_hi": {
                            "type": "STRING"
                        },
                        "chemical": {
                            "type": "STRING"
                        },
                        "organic": {
                            "type": "STRING"
                        },
                        "prevention": {
                            "type": "STRING"
                        },
                        "crop_stage": {
                            "type": "STRING"
                        }
                    },
                    "required": [
                        "pest",
                        "common_name_en",
                        "common_name_hi",
                        "chemical",
                        "organic",
                        "prevention",
                        "crop_stage"
                    ]
                }
            )
        )

        # Get response text
        response_text = response.text.strip()

        # Parse JSON
        advice = json.loads(response_text)

        return advice

    except json.JSONDecodeError as e:

        return {
            "error": "Gemini returned invalid JSON.",
            "details": str(e),
            "raw": response.text if response else ""
        }

    except Exception as e:

        return {
            "error": "Gemini API request failed.",
            "details": str(e)
        }


# ============================================================
# TEST FUNCTION
# ============================================================

if __name__ == "__main__":

    print("Testing Gemini connection...")

    test_pest = "Apolygus lucorum"

    result = get_advice(test_pest)

    print("\nGemini Response:")
    print(json.dumps(result, indent=4, ensure_ascii=False))