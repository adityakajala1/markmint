from typing import Any, BinaryIO
import pdfplumber
import logging

# Suppress noisy PDFMiner font warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)


class PDFParser:
    """Handles deterministic text extraction from PDFs."""

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
                    if text:
                        pages_data.append({"page_number": i + 1, "text": text})
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

        return pages_data
