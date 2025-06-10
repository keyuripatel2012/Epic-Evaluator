from typing import Optional

def extract_text_from_file(file) -> Optional[str]:
    """
    Extracts clean, normalized text from uploaded file (txt, pdf, docx).
    """
    filename = file.name.lower()
    try:
        if filename.endswith(".txt"):
            file.seek(0)
            content = file.read().decode("utf-8")
            return content

        elif filename.endswith(".pdf"):
            import fitz  # PyMuPDF
            file.seek(0)
            pdf_bytes = file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in pdf_document:
                text += page.get_text("text")  # ensures layout-preserved text
            return _normalize_text(text)

        elif filename.endswith(".docx"):
            from docx import Document
            file.seek(0)
            document = Document(file)
            paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)

        else:
            return None
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return None


def _normalize_text(text: str) -> str:
    """
    Normalize extracted text from PDFs to ensure parsing works correctly.
    """
    import re
    # Remove multiple spaces, fix line breaks around dashes/bullets
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n([\-•])", r" \1", text)  # keep bullets on same line
    text = re.sub(r"\n+", "\n", text)
    return text.strip()
