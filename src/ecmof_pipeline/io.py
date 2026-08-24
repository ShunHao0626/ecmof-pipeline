"""JSON input/output helpers used by the EC-MOF pipeline."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterator


def strip_error_comments(text: str) -> str:
    """Remove legacy ``//error`` comments without touching JSON strings.

    Earlier research files used ``//error`` as an inline review marker. JSON does
    not permit comments, so this function removes only comments whose first token
    is exactly ``//error``. Other JavaScript-style comments remain invalid.
    """

    result: list[str] = []
    index = 0
    in_string = False
    escaped = False

    while index < len(text):
        char = text[index]

        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue

        if text.startswith("//error", index):
            newline = text.find("\n", index)
            if newline == -1:
                break
            result.append("\n")
            index = newline + 1
            continue

        result.append(char)
        index += 1

    return "".join(result)


def load_json(path: str | Path, *, allow_error_comments: bool = True) -> Any:
    """Load UTF-8 JSON, optionally repairing legacy ``//error`` markers."""

    source = Path(path)
    text = source.read_text(encoding="utf-8-sig")
    if allow_error_comments:
        text = strip_error_comments(text)
    return json.loads(text)


def write_json(path: str | Path, value: Any) -> None:
    """Write JSON atomically using UTF-8 and stable human-readable formatting."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary_name, destination)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def iter_json_files(path: str | Path) -> Iterator[Path]:
    """Yield one JSON file or every JSON file below a directory."""

    source = Path(path)
    if source.is_file():
        yield source
        return
    if not source.is_dir():
        raise FileNotFoundError(f"JSON input does not exist: {source}")
    yield from sorted(source.rglob("*.json"))
