class QuestionNormalizer:
    """
    Strips irrelevant punctuation, standardizes whitespace, and lowercases the text
    for exact lexical hashing. Preserves mathematical and LaTeX notation.
    """
    
    # Unicode sub/superscript mapping
    SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾", "0123456789+-=()")
    SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎", "0123456789+-=()")

    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
            
        # Lowercase
        normalized = text.lower()
        
        # Remove markdown artifacts if any
        normalized = normalized.replace("**", "").replace("*", "")
        
        # Map unicode superscripts and subscripts to LaTeX-like equivalents
        # e.g., x² -> x^2, H₂ -> H_2
        for char, mapped in zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾", "0123456789+-=()"):
            normalized = normalized.replace(char, f"^{mapped}")
        for char, mapped in zip("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎", "0123456789+-=()"):
            normalized = normalized.replace(char, f"_{mapped}")
            
        # Punctuation we want to STRIP (ordinary English punctuation)
        # But we KEEP math symbols: + - = < > ^ _ \ { } [ ] ( ) / *
        # So we only strip things like , . ; : ! ? ' "
        chars_to_strip = ",.;:!?'\"“”‘’"
        translator = str.maketrans('', '', chars_to_strip)
        normalized = normalized.translate(translator)
        
        # Standardize whitespace (collapse multiple spaces/newlines to single space)
        import re
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
