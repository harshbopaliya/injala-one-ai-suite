# ocr_utils.py

import io
from typing import List
import pytesseract
from PIL import Image, ImageOps
import fitz  # PyMuPDF

class OCRProcessingError(Exception):
    """Custom exception for OCR or PDF processing failures."""
    pass

# ✅ Explicit Tesseract path for Streamlit deployments
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ✅ Confirm Tesseract availability on startup
try:
    tess_version = pytesseract.get_tesseract_version()
    print(f"[INFO] Tesseract version: {tess_version}")
except Exception as e:
    print(f"[ERROR] Tesseract not accessible: {e}")

def extract_images_from_pdf(file_bytes: bytes) -> List[Image.Image]:
    """
    Extracts high-resolution images from each page of a PDF.

    Args:
        file_bytes (bytes): PDF file content in binary format.

    Returns:
        List[Image.Image]: List of PIL Image objects, one per page.

    Raises:
        OCRProcessingError: If PDF processing fails.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        images = []

        for page_number, page in enumerate(doc, start=1):
            try:
                pix = page.get_pixmap(dpi=400, alpha=False)  # ✅ Higher DPI for better OCR
                img_bytes = io.BytesIO(pix.tobytes("png"))
                images.append(Image.open(img_bytes).convert("RGB"))
            except Exception as e:
                print(f"[WARN] Failed to extract image from page {page_number}: {e}")
                continue

        if not images:
            raise OCRProcessingError("No images could be extracted from the PDF.")

        return images

    except Exception as e:
        raise OCRProcessingError(f"Failed to read PDF: {e}") from e

def run_ocr_on_images(images: List[Image.Image], lang: str = "eng") -> str:
    """
    Runs OCR on a list of images using Tesseract.

    Args:
        images (List[Image.Image]): List of PIL Image objects.
        lang (str, optional): Language code for OCR (default: 'eng').

    Returns:
        str: Combined extracted text from all images.

    Raises:
        OCRProcessingError: If OCR fails on all images.
    """
    extracted_text = []
    config = "--psm 6"  # Assume a uniform block of text for best page OCR

    for idx, img in enumerate(images, start=1):
        try:
            # ✅ Convert to grayscale
            gray_img = ImageOps.grayscale(img)

            # ✅ Optional: Binarize for better OCR accuracy
            bin_img = gray_img.point(lambda x: 0 if x < 128 else 255, '1')

            # ✅ Run OCR
            text = pytesseract.image_to_string(bin_img, lang=lang, config=config)

            if not text.strip():
                # ✅ Save debug image for manual inspection
                debug_filename = f"debug_page_{idx}.png"
                bin_img.save(debug_filename)
                print(f"[DEBUG] Saved {debug_filename} for inspection (empty OCR output).")

            extracted_text.append(text.strip())

        except Exception as e:
            print(f"[WARN] OCR failed on image {idx}: {e}")
            extracted_text.append("")

    combined_text = "\n\n".join(filter(None, extracted_text)).strip()

    if not combined_text:
        raise OCRProcessingError("OCR did not extract any text from the images.")

    return combined_text
