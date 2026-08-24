"""Command-line interface for the EC-MOF pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .convert import convert_path
from .io import load_json, write_json
from .literature import extract_text, iter_documents, split_text
from .normalize import collect_records, flatten_records, normalize_record
from .validate import validate_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ecmof-pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="Convert local PDFs to Markdown")
    convert_parser.add_argument("--input", required=True)
    convert_parser.add_argument("--output", required=True)

    normalize_parser = subparsers.add_parser("normalize", help="Normalize JSON records")
    normalize_parser.add_argument("--input", required=True, action="append")
    normalize_parser.add_argument("--output", required=True)

    validate_parser = subparsers.add_parser("validate", help="Match JSON fields to documents")
    validate_parser.add_argument("--data", required=True)
    validate_parser.add_argument("--papers", required=True)
    validate_parser.add_argument("--report", required=True)
    validate_parser.add_argument("--threshold", type=float, default=0.8)
    validate_parser.add_argument("--chunk-size", type=int, default=1_500)

    return parser


def _run_convert(args: argparse.Namespace) -> int:
    outputs = convert_path(args.input, args.output)
    print(f"Converted {len(outputs)} PDF file(s).")
    return 0


def _run_normalize(args: argparse.Namespace) -> int:
    records = collect_records(args.input)
    write_json(args.output, records)
    print(f"Wrote {len(records)} normalized record(s) to {args.output}.")
    return 0


def _run_validate(args: argparse.Namespace) -> int:
    value = load_json(args.data)
    records = [normalize_record(record) for record in flatten_records(value)]

    chunks: list[str] = []
    for document in iter_documents(args.papers):
        chunks.extend(split_text(extract_text(document), chunk_size=args.chunk_size))
    if not chunks:
        raise RuntimeError("No text could be extracted from the supplied documents")

    report = validate_records(records, chunks, threshold=args.threshold)
    write_json(args.report, report)
    summary = report["summary"]
    print(
        f"Checked {summary['fields_checked']} field(s); "
        f"matched {summary['fields_matched']}. Report: {args.report}"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "convert":
        return _run_convert(args)
    if args.command == "normalize":
        return _run_normalize(args)
    if args.command == "validate":
        return _run_validate(args)
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
