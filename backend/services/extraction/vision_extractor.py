import os
import json
from typing import Any, Optional
from pydantic import BaseModel, Field

from google import genai
from google.genai import types

from backend.schemas import (
    DocumentExtractionResult,
    ExtractedSection,
    ExtractedQuestion,
)


class GeminiSubSubquestion(BaseModel):
    number: str = Field(description="Sub-subquestion number/letter, e.g. 'i'")
    text: str = Field(description="Text. Preserve math notation.")
    marks: Optional[float] = Field(None, description="Marks if any.")

class GeminiSubquestion(BaseModel):
    number: str = Field(description="Subquestion number/letter, e.g. 'a'")
    text: str = Field(description="Text. Preserve math notation.")
    marks: Optional[float] = Field(None, description="Marks if any.")
    subquestions: list[GeminiSubSubquestion] = Field(default_factory=list, description="Further nested subquestions.")

class GeminiAlternativeQuestion(BaseModel):
    number: str = Field(description="Main question number, e.g. '1', '2'")
    text: str = Field(description="Text of the question. Preserve math notation.")
    marks: Optional[float] = Field(None, description="Marks for the question, if any.")
    subquestions: list[GeminiSubquestion] = Field(default_factory=list, description="Subquestions belonging to this question.")

class GeminiQuestion(BaseModel):
    number: str = Field(description="Main question number, e.g. '1', '2'")
    text: str = Field(description="Text of the question. Preserve math notation.")
    marks: Optional[float] = Field(None, description="Marks for the question, if any.")
    subquestions: list[GeminiSubquestion] = Field(default_factory=list, description="Subquestions belonging to this question.")
    or_alternative: Optional[GeminiAlternativeQuestion] = Field(None, description="If this question has an 'OR' alternative, nest it here.")

class GeminiSection(BaseModel):
    name: str = Field(description="Name of the section, e.g. 'PART A', 'Section 1'")
    instructions: Optional[str] = Field(None, description="Instructions for this section.")
    questions: list[GeminiQuestion] = Field(default_factory=list)

class GeminiDocumentMetadata(BaseModel):
    assessment_type: Optional[str] = Field(None, description="e.g., 'CT1', 'CT2', 'END_SEM', 'MID_SEM', 'MODEL', 'UNKNOWN'. Look at the visible headings/title. Do NOT guess.")
    year: Optional[int] = Field(None, description="e.g. 2023. Extract from visible text. Do not guess.")

class GeminiDocument(BaseModel):
    metadata: Optional[GeminiDocumentMetadata] = Field(None, description="Global document metadata")
    sections: list[GeminiSection]


class VisionExtractor:
    """Multimodal vision-based document extractor using Gemini 1.5 Flash / 3.x Flash."""

    @classmethod
    def extract_pdf(cls, file_path: str) -> DocumentExtractionResult:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return DocumentExtractionResult(
                sections=[],
                total_pages=0,
                successful=False,
                error_message="GEMINI_API_KEY not found in environment."
            )

        client = genai.Client()

        # Upload the PDF via the Files API
        try:
            print(f"[VisionExtractor] Uploading {file_path} to Gemini...")
            # We must use client.files.upload
            gemini_file = client.files.upload(
                file=file_path,
                config={"display_name": os.path.basename(file_path)}
            )
            
            # Wait for processing if needed
            while gemini_file.state.name == "PROCESSING":
                import time
                time.sleep(2)
                gemini_file = client.files.get(name=gemini_file.name)
            
            if gemini_file.state.name == "FAILED":
                return DocumentExtractionResult(
                    sections=[],
                    total_pages=0,
                    successful=False,
                    error_message="Gemini file processing failed."
                )

        except Exception as e:
            return DocumentExtractionResult(
                sections=[],
                total_pages=0,
                successful=False,
                error_message=f"Failed to upload PDF to Gemini: {str(e)}"
            )

        prompt = """
        You are an expert academic document parser. 
        Extract all exam questions from this document. 
        Preserve the exact hierarchical structure (Sections -> Questions -> Subquestions -> Sub-subquestions).
        If there is an "OR" choice between two questions, place the second question inside the `or_alternative` field of the first question.
        
        CRITICAL RULES FOR STEM/MATH:
        1. Preserve all mathematical notation, formulas, matrices, integrals, superscripts, subscripts, Greek letters, and chemical equations exactly. Use LaTeX notation for math (e.g., \\frac{dy}{dx}, \\int_0^\\pi).
        2. Do NOT convert mathematical equations into flat ASCII garbage.
        3. Extract the exact marks (e.g. 5, 10) if they are explicitly present.
        4. Do NOT hallucinate questions that do not exist.
        """

        try:
            print("[VisionExtractor] Generating structured content...")
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[gemini_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GeminiDocument,
                    temperature=0.1
                )
            )
            
            output_text = response.text
            data = json.loads(output_text)
            
            # Transform to internal schema
            return cls._transform_to_domain(data)
            
        except Exception as e:
            return DocumentExtractionResult(
                sections=[],
                total_pages=0,
                successful=False,
                error_message=f"Gemini API error: {str(e)}"
            )
        finally:
            try:
                client.files.delete(name=gemini_file.name)
            except:
                pass


    @classmethod
    def _transform_to_domain(cls, data: dict) -> DocumentExtractionResult:
        sections: list[ExtractedSection] = []
        
        for sec_data in data.get("sections", []):
            ext_questions: list[ExtractedQuestion] = []
            
            for q_data in sec_data.get("questions", []):
                q_text = cls._flatten_question_text(q_data)
                
                # We don't have page numbers natively from this schema, default to 1
                page_number = 1
                confidence = 0.9 # High base confidence if vision succeeded
                
                # Heuristic for needs_review (e.g., if it still contains obvious OCR garbage)
                needs_review = "[UNRECOGNIZED" in q_text
                
                # Check for OR alternative
                is_alternative = False
                
                ext_q = ExtractedQuestion(
                    question_number=q_data.get("number", ""),
                    original_text=q_text,
                    structured_content=q_data,
                    marks=q_data.get("marks"),
                    is_alternative=is_alternative,
                    page_number=page_number,
                    confidence=confidence,
                    needs_review=needs_review,
                    extraction_method="vision_gemini"
                )
                ext_questions.append(ext_q)
                
                # Add the OR alternative as a separate question marked is_alternative=True
                or_alt = q_data.get("or_alternative")
                if or_alt:
                    alt_text = cls._flatten_question_text(or_alt)
                    alt_q = ExtractedQuestion(
                        question_number=or_alt.get("number", ""),
                        original_text=alt_text,
                        structured_content=or_alt,
                        marks=or_alt.get("marks"),
                        is_alternative=True,
                        page_number=page_number,
                        confidence=confidence,
                        needs_review="[UNRECOGNIZED" in alt_text,
                        extraction_method="vision_gemini"
                    )
                    ext_questions.append(alt_q)

            sections.append(
                ExtractedSection(
                    name=sec_data.get("name", "General"),
                    instructions=sec_data.get("instructions"),
                    questions=ext_questions
                )
            )
            
        return DocumentExtractionResult(
            sections=sections,
            total_pages=1, # We don't track total pages via the LLM response right now
            successful=True,
            assessment_type=data.get("metadata", {}).get("assessment_type") if data.get("metadata") else None,
            year=data.get("metadata", {}).get("year") if data.get("metadata") else None
        )

    @classmethod
    def _flatten_question_text(cls, q_data: dict, indent_level: int = 0) -> str:
        """Render the structured question back into a readable markdown string."""
        indent = "  " * indent_level
        lines = []
        
        num = q_data.get("number", "")
        text = q_data.get("text", "")
        marks = q_data.get("marks")
        
        header = f"{indent}{num}. {text}"
        if marks is not None:
            header += f" [{marks}]"
            
        lines.append(header)
        
        for sub in q_data.get("subquestions", []):
            lines.append(cls._flatten_question_text(sub, indent_level + 1))
            
        return "\n".join(lines)

