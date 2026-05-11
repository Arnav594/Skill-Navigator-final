"""Tests for services/file_service.py — malformed/unsupported upload handling.

We use a tiny FakeFile that mimics Flask's FileStorage interface
(filename + read()) without needing real PDFs on disk.
"""
import io
from services.file_service import parse_uploaded_file


class FakeFile:
    """Minimal stand-in for werkzeug.FileStorage."""
    def __init__(self, filename: str, content: bytes = b""):
        self.filename = filename
        self._buffer = io.BytesIO(content)

    def read(self):
        return self._buffer.read()


def test_unsupported_file_type_returns_friendly_error():
    """A .txt upload should return a user-friendly error, not crash."""
    text, error = parse_uploaded_file(FakeFile("resume.txt", b"some text"))
    assert text is None
    assert error is not None
    assert "Unsupported file type" in error


def test_malformed_pdf_returns_friendly_error():
    """A file with .pdf extension but garbage bytes should not raise — it should
    return a clean error message instead.
    """
    text, error = parse_uploaded_file(FakeFile("broken.pdf", b"this is not a real pdf"))
    assert text is None
    assert error is not None
    assert "Failed" in error or "Could not" in error
