import json
from typing import Optional, Dict, Any

class CanonicalRepresentationBuilder:
    """
    Transforms the JSON structured_content of a Question into a high-fidelity
    canonical string for NLP matching, embeddings, and classification.
    Preserves LaTeX, mathematical notation, and meaningful hierarchy.
    """
    
    @staticmethod
    def build(question) -> str:
        if not question.structured_content:
            return question.original_text or ""
            
        data = question.structured_content
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return question.original_text or ""

        return CanonicalRepresentationBuilder._flatten_question(data).strip()

    @staticmethod
    def _flatten_question(q_data: Dict[str, Any], indent_level: int = 0) -> str:
        indent = "    " * indent_level
        lines = []
        
        # Question can have question_number (old schema) or number (new schema)
        q_num = q_data.get("question_number", q_data.get("number", ""))
        q_text = q_data.get("original_text", q_data.get("text", ""))
        
        if q_num and q_text:
            lines.append(f"{indent}{q_num}. {q_text}")
        elif q_text:
            lines.append(f"{indent}{q_text}")
            
        # Add subquestions
        subs = q_data.get("subquestions", [])
        for sub in subs:
            s_num = sub.get("number", "")
            s_text = sub.get("text", "")
            if s_num and s_text:
                lines.append(f"{indent}    ({s_num}) {s_text}")
            elif s_text:
                lines.append(f"{indent}    {s_text}")
                
            # sub-subquestions
            subsubs = sub.get("subquestions", [])
            for subsub in subsubs:
                ss_num = subsub.get("number", "")
                ss_text = subsub.get("text", "")
                if ss_num and ss_text:
                    lines.append(f"{indent}        ({ss_num}) {ss_text}")
                elif ss_text:
                    lines.append(f"{indent}        {ss_text}")

        # OR Alternative
        alt = q_data.get("or_alternative")
        if alt:
            lines.append(f"{indent}    --- OR ---")
            alt_lines = CanonicalRepresentationBuilder._flatten_question(alt, indent_level + 1)
            lines.append(alt_lines)
            
        return "\n".join(lines)
