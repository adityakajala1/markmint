from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any

from app.schemas import DocumentExtractionResult
from app.services.extraction.pdf_parser import PDFParser
from app.services.extraction.question_extractor import QuestionExtractor

router = APIRouter()


@router.post("/papers/upload", response_model=DocumentExtractionResult)
async def upload_paper(file: UploadFile = File(...)) -> Any:
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Read the file into memory
        pages_data = PDFParser.extract_text_with_pages(file.file)

        # Extract questions
        result = QuestionExtractor.extract(pages_data)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
