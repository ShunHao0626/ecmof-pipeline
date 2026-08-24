"""Lightweight checks for the draft EC-MOF record schema."""

from __future__ import annotations

from typing import Any


EXPECTED_FIELDS = (
    "MOF_name",
    "molecular_formula",
    "source_paper",
    "metal_node",
    "ligand",
    "topology",
    "Dimensionality",
    "Crystal_system",
    "Space_group",
    "properties",
    "characterization_data",
    "synthesis_method",
    "reaction_conditions",
    "raw_materials",
    "composition_structure",
    "application",
)


def check_record(record: Any) -> list[str]:
    """Return human-readable schema problems for one record."""

    if not isinstance(record, dict):
        return [f"record must be an object, got {type(record).__name__}"]

    problems = []
    for field in EXPECTED_FIELDS:
        if field not in record:
            problems.append(f"missing field: {field}")

    for field in ("metal_node", "ligand"):
        if field in record and not isinstance(record[field], dict):
            problems.append(f"{field} should be an object")

    return problems
