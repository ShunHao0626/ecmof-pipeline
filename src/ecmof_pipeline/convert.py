"""Optional local PDF-to-Markdown conversion."""

from __future__ import annotations

from pathlib import Path


def convert_pdf(pdf_path: str | Path, output_path: str | Path) -> Path:
    """Convert one local PDF with pymupdf4llm and return the Markdown path."""

    try:
        import pymupdf4llm
    except ImportError as error:
        raise RuntimeError(
            "PDF conversion is optional. Install it with: pip install -e '.[pdf]'"
        ) from error

    source = Path(pdf_path)
    if not source.is_file() or source.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {source}")

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    markdown = pymupdf4llm.to_markdown(str(source))
    destination.write_text(markdown, encoding="utf-8")
    return destination


def convert_path(input_path: str | Path, output_dir: str | Path) -> list[Path]:
    """Convert one PDF or all PDFs below a directory."""

    source = Path(input_path)
    destination = Path(output_dir)
    if source.is_file():
        return [convert_pdf(source, destination / f"{source.stem}.md")]
    if not source.is_dir():
        raise FileNotFoundError(f"PDF input does not exist: {source}")

    outputs = []
    for pdf_path in sorted(source.rglob("*.pdf")):
        relative = pdf_path.relative_to(source).with_suffix(".md")
        outputs.append(convert_pdf(pdf_path, destination / relative))
    return outputs
