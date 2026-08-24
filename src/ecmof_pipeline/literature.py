"""Read local research documents without redistributing their contents."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


TEXT_SUFFIXES = {".md", ".txt"}


def iter_documents(path: str | Path) -> Iterator[Path]:
    """Yield supported documents from a file or directory."""

    source = Path(path)
    if source.is_file():
        yield source
        return
    if not source.is_dir():
        raise FileNotFoundError(f"Document input does not exist: {source}")
    for candidate in sorted(source.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES | {".pdf"}:
            yield candidate


def extract_text(path: str | Path) -> str:
    """Extract text from Markdown, plain text, or a PDF using pdfplumber."""

    source = Path(path)
    if source.suffix.lower() in TEXT_SUFFIXES:
        return source.read_text(encoding="utf-8", errors="replace")
    if source.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported document type: {source.suffix}")

    try:
        import pdfplumber
    except ImportError as error:
        raise RuntimeError(
            "PDF support is optional. Install it with: pip install -e '.[pdf]'"
        ) from error

    pages: list[str] = []
    with pdfplumber.open(source) as document:
        for page in document.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


def split_text(text: str, *, chunk_size: int = 1_500, overlap: int = 150) -> list[str]:
    """Split text into overlapping chunks for local evidence matching."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    compact = " ".join(text.split())
    if not compact:
        return []

    step = chunk_size - overlap
    return [compact[start : start + chunk_size] for start in range(0, len(compact), step)]
