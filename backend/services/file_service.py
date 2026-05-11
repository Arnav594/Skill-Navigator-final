"""Parse uploaded resume files (PDF or DOCX) into plain text.

Returns (text, error). If error is set, text is None and the caller should
surface a 400 response. Errors are user-friendly strings, not stack traces.
"""
import fitz   # PyMuPDF
import docx


def parse_uploaded_file(file) -> tuple[str | None, str | None]:
    """Extract text from an uploaded PDF or DOCX file.

    Returns (text, error). Exactly one of them is non-None.
    """
    filename = file.filename.lower()
    try:
        if filename.endswith(".pdf"):
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in pdf:
                text += page.get_text()
            if not text.strip():
                return None, "Could not extract text from PDF. Please paste your resume manually."
            return text.strip(), None

        elif filename.endswith(".docx"):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            if not text.strip():
                return None, "Could not extract text from Word file. Please paste your resume manually."
            return text.strip(), None

        else:
            return None, "Unsupported file type. Please upload a PDF or Word (.docx) file."

    except Exception as e:
        print("File parse error:", e)
        return None, "Failed to read the file. Please paste your resume text manually."
