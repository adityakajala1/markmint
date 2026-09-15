from typing import Any, BinaryIO
import pdfplumber
import logging
import numpy as np

# Suppress noisy PDFMiner font warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)

class OCRReader:
    _reader = None
    
    @classmethod
    def get_reader(cls):
        if cls._reader is None:
            import easyocr
            cls._reader = easyocr.Reader(['en'], verbose=False)
        return cls._reader

class PDFParser:
    """Handles deterministic text extraction from PDFs."""

    @staticmethod
    def extract_structured(file_stream: BinaryIO) -> dict[str, Any]:
        pages_data = PDFParser.extract_text_with_pages(file_stream)
        structured = {
            "pages": pages_data,
            "tables": [],
            "images": [],
            "equations": [],
        }
        return structured

    @staticmethod
    def is_scanned_page(page, text: str) -> bool:
        """Determines if a page is a scanned image."""
        text_len = len((text or "").strip())
        if text_len < 100:
            if len(page.images) > 0:
                return True
        return False

    @staticmethod
    def _perform_ocr(page) -> str:
        """Performs OCR on a single pdfplumber page using easyocr."""
        try:
            im = page.to_image(resolution=150)
            img_data = np.array(im.original)
            
            reader = OCRReader.get_reader()
            result = reader.readtext(img_data)
            
            # Sort by vertical position (y_min)
            sorted_res = sorted(result, key=lambda r: (r[0][0][1], r[0][0][0]))
            
            lines = []
            for (bbox, text, prob) in sorted_res:
                if prob > 0.4:
                    lines.append(text)
                elif prob > 0.1:
                    # Likely a complex equation or diagram that OCR cannot faithfully reconstruct
                    lines.append("[UNRECOGNIZED_MATH_REGION]")
                    
            return "\n".join(lines)
        except Exception as e:
            logging.error(f"OCR failed on page: {e}")
            return ""

    @staticmethod
    def extract_text_with_pages(file_stream: BinaryIO) -> list[dict[str, Any]]:
        """
        Extracts text page by page.
        Returns a list of dicts: [{'page_number': 1, 'text': '...'}, ...]
        """
        pages_data: list[dict[str, Any]] = []
        try:
            with pdfplumber.open(file_stream) as pdf:  # type: ignore
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    
                    if PDFParser.is_scanned_page(page, text):
                        print(f"  [OCR] Processing scanned page {i+1}...")
                        ocr_text = PDFParser._perform_ocr(page)
                        if ocr_text:
                            text = ocr_text
                            
                    if text:
                        pages_data.append({"page_number": i + 1, "text": text})
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

        return pages_data
