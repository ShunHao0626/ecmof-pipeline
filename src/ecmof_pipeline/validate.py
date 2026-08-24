"""Evidence matching for structured EC-MOF fields."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from typing import Any, Iterator


def normalize_text(value: Any) -> str:
    """Normalize a scalar value for evidence matching."""

    text = unicodedata.normalize("NFKC", str(value)).casefold()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def iter_scalar_fields(value: Any, prefix: str = "") -> Iterator[tuple[str, Any]]:
    """Yield dotted paths and scalar leaves from a nested record."""

    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield from iter_scalar_fields(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            path = f"{prefix}[{index}]"
            yield from iter_scalar_fields(child, path)
    elif value is not None:
        yield prefix, value


def _partial_similarity(needle: str, haystack: str) -> float:
    if not needle or not haystack:
        return 0.0
    if needle in haystack:
        return 1.0
    match = SequenceMatcher(None, needle, haystack, autojunk=False).find_longest_match()
    return match.size / len(needle)


def best_evidence(value: Any, chunks: list[str]) -> tuple[float, int | None]:
    """Return the best lexical evidence score and chunk index."""

    needle = normalize_text(value)
    best_score = 0.0
    best_index = None
    for index, chunk in enumerate(chunks):
        score = _partial_similarity(needle, normalize_text(chunk))
        if score > best_score:
            best_score = score
            best_index = index
        if score == 1.0:
            break
    return best_score, best_index


def validate_records(
    records: list[dict[str, Any]], chunks: list[str], *, threshold: float = 0.8
) -> dict[str, Any]:
    """Validate scalar record fields against local document chunks."""

    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")

    checked = 0
    matched = 0
    record_reports = []

    for index, record in enumerate(records):
        fields = {}
        for path, value in iter_scalar_fields(record):
            if isinstance(value, (str, int, float)) and str(value).strip():
                score, chunk_index = best_evidence(value, chunks)
                status = "matched" if score >= threshold else "unmatched"
                checked += 1
                matched += status == "matched"
                fields[path] = {
                    "status": status,
                    "score": round(score, 4),
                    "chunk_index": chunk_index,
                }
        record_reports.append(
            {
                "index": index,
                "MOF_name": record.get("MOF_name"),
                "fields": fields,
            }
        )

    return {
        "summary": {
            "records": len(records),
            "fields_checked": checked,
            "fields_matched": matched,
            "fields_unmatched": checked - matched,
            "threshold": threshold,
        },
        "records": record_reports,
    }
