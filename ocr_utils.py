import cv2
import easyocr
import numpy as np
from PIL import Image
import traceback

# Initialize reader once
try:
    reader = easyocr.Reader(['en'], gpu=False)
except Exception as e:
    print(f"Error initializing EasyOCR: {e}")
    reader = None

def preprocess_for_easyocr(pil_image: Image.Image) -> np.ndarray:
    # Ensure image is RGB (avoids crashes on PNGs with transparency/RGBA)
    rgb_img = pil_image.convert("RGB")
    img = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)

    # 1. More aggressive upscaling if the image is small (better OCR)
    h, w = img.shape[:2]
    if max(h, w) < 1500:
        scale_factor = 1500 / max(h, w)
        img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # 2. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Enhanced Denoising
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # 4. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # Increased clipLimit for stronger contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # 5. Sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    return sharpened


def reconstruct_lines(results, y_tolerance: int = 20, min_conf: float = 0.2) -> str:
    """Groups words on the same horizontal row together."""
    valid = [item for item in results if item[2] >= min_conf]
    # Sort top-to-bottom by top-left Y coordinate
    valid.sort(key=lambda x: x[0][0][1])

    rows = []
    for bbox, text, conf in valid:
        # Using middle Y point for grouping
        y_center = (bbox[0][1] + bbox[2][1]) / 2
        x_left = bbox[0][0]

        placed = False
        for row in rows:
            if abs(row["y"] - y_center) <= y_tolerance:
                row["items"].append((x_left, text))
                # Update y_center to be the average of the row to avoid drift
                row["y"] = (row["y"] + y_center) / 2
                placed = True
                break
        if not placed:
            rows.append({"y": y_center, "items": [(x_left, text)]})

    # Sort each row left-to-right and join words with spaces
    formatted_lines = []
    for row in rows:
        row["items"].sort(key=lambda item: item[0])
        formatted_lines.append(" ".join(text for _, text in row["items"]))

    return "\n".join(formatted_lines)


def perform_ocr(image_file):
    if reader is None:
        raise Exception("EasyOCR reader not initialized.")
    try:
        raw_image = Image.open(image_file)
        processed_image = preprocess_for_easyocr(raw_image)
        
        results = reader.readtext(
            processed_image,
            detail=1,
            paragraph=False,
            mag_ratio=1.5,          # Increased for better small-text detection
            contrast_ths=0.2,       # More robust to background noise
            adjust_contrast=0.8,
            text_threshold=0.5,     # Slightly more permissive
            low_text=0.3,
            decoder='beamsearch',
            beamWidth=15            # Larger beam width for better accuracy
        )
        
        return reconstruct_lines(results, y_tolerance=20, min_conf=0.25)
    except Exception as e:
        return f"Error performing OCR: {str(e)}\n{traceback.format_exc()}"
