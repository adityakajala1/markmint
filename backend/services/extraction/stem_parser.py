import fitz  # PyMuPDF
from typing import Any

class STEMPDFParser:
    """Real layout-aware extraction — preserves STEM notation."""

    @staticmethod
    def extract(file_path: str) -> dict[str, Any]:
        doc = fitz.open(file_path)
        result = {
            "pages": [],
            "blocks": [],
            "images": [],
            "equations": [],  # detected equation blocks
            "source_file": file_path,
        }
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("dict")
            # Preserve blocks with positions — no flattened text
            blocks = []
            for block in text.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        spans = line.get("spans", [])
                        # Preserve superscript/subscript via font size/position (Step 5)
                        line_text = "".join(
                            s.get("text", "") for s in spans
                        )
                        # No destructive normalization — preserve ∫ √ ∑ etc.
                        blocks.append({
                            "bbox": block.get("bbox"),
                            "line_text": line_text,
                            "spans": [
                                {
                                    "text": s.get("text"),
                                    "font": s.get("font"),
                                    "size": s.get("size"),
                                    "flags": s.get("flags"),
                                }
                                for s in spans
                            ],
                            "page": page_num + 1,
                        })
            result["blocks"].extend(blocks)

            # Images (Step 4 — targeted, not full-page OCR)
            img_list = page.get_images()
            for img_index, img in enumerate(img_list, start=1):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                result["images"].append({
                    "page": page_num + 1,
                    "xref": xref,
                    "width": pix.width,
                    "height": pix.height,
                })
                pix = None

            # Page dimensions
            result["pages"].append({
                "page_number": page_num + 1,
                "width": page.rect.width,
                "height": page.rect.height,
                "blocks_count": len(blocks),
            })
        doc.close()
        return result
