import requests
import base64
import io
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import re

OCR_API_KEY = "K81494913188957"

def preprocess_pil_image(pil_image):
    # Save the original image for debugging
    pil_image.save("captcha_original.png")

    image = pil_image.convert("L")
    image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.5)
    open_cv_image = np.array(image)
    _, binary = cv2.threshold(open_cv_image, 150, 255, cv2.THRESH_BINARY)
    processed = Image.fromarray(binary)

    # Save processed image for inspection
    processed.save("captcha_processed.png")
    return processed

def solve_captcha_with_ocr_space(pil_image, log_event=None):
    try:
        processed_image = preprocess_pil_image(pil_image)
        buffered = io.BytesIO()
        processed_image.save(buffered, format="PNG")
        base64_img = base64.b64encode(buffered.getvalue()).decode()

        payload = {
            "apikey": OCR_API_KEY,
            "base64Image": "data:image/png;base64," + base64_img,
            "language": "eng",
            "OCREngine": 2,
            "isOverlayRequired": False,
            "scale": True
        }
        response = requests.post("https://api.ocr.space/parse/image", data=payload)
        result = response.json()
        parsed_text = result.get("ParsedResults", [{}])[0].get("ParsedText", "").strip()

        # Log raw OCR output
        if log_event:
            log_event("captcha_ocr_raw", f"Raw OCR text: '{parsed_text}'")

        parsed_text = parsed_text.replace(" ", "").replace("\n", "")
        cleaned_text = re.sub(r'[^A-Za-z0-9=+\-*/]', '', parsed_text)

        if 5 <= len(cleaned_text) <= 6:
            if log_event:
                log_event("captcha_ocr_success", f"OCR solved: {cleaned_text}")
            return cleaned_text
        else:
            if log_event:
                log_event("captcha_ocr_invalid", f"OCR returned unexpected length: {parsed_text}")
            return ""
    except Exception as e:
        if log_event:
            log_event("captcha_ocr_exception", f"OCR error: {e}")
        return ""
