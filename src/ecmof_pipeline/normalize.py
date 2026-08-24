"""Normalize fragmented or accidentally nested EC-MOF JSON records."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Iterator

from .io import iter_json_files, load_json
from .schema import EXPECTED_FIELDS


def flatten_records(value: Any) -> Iterator[dict[str, Any]]:
    """Recursively flatten lists and yield every object as a record."""

    if isinstance(value, dict):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_records(item)
    else:
        raise TypeError(
            f"Expected a JSON object or array of objects, got {type(value).__name__}"
        )


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a stable field order while preserving unexpected source fields."""

    normalized = {field: record.get(field) for field in EXPECTED_FIELDS}
    for key, value in record.items():
        if key not in normalized:
            normalized[key] = value
    return normalized


def collect_records(inputs: Iterable[str | Path]) -> list[dict[str, Any]]:
    """Load, repair, flatten, and normalize records from files or directories."""

    records: list[dict[str, Any]] = []
    for input_path in inputs:
        for json_file in iter_json_files(input_path):
            value = load_json(json_file)
            records.extend(normalize_record(record) for record in flatten_records(value))
    return records
