# EC-MOF Data Pipeline

**English** · [简体中文](README_CN.md)

**Research problem.** Conductive metal-organic framework (EC-MOF) properties are reported across papers in inconsistent formats, making structured comparison and source checking laborious.

I built a Python pipeline that normalizes extracted MOF records and locates candidate supporting text in source papers. The repository includes a **71-record research dataset citing 21 sources**, a draft schema, command-line tools, and tests. Its evidence report helps prioritize field-by-field scientific review.

## Research artifacts

The workflow connects structured records to lexical evidence from locally held papers. These research annotations can then be reviewed field by field against the source.

| Component | Status |
| --- | --- |
| PDF-to-Markdown conversion | Available as an optional feature |
| Structured MOF records | 71-record draft snapshot included |
| Exact and fuzzy (lexical) evidence matching | Available |
| Command-line interface | Available |
| Automated tests | Included |

## Goals

- Convert locally obtained papers into machine-readable text for private research.
- Represent structural, synthetic, characterization, and property information in
  a consistent JSON schema.
- Compare extracted values with source documents through exact and fuzzy lexical matching.
- Record validation evidence without inserting invalid comments into JSON files.
- Produce a small, reproducible dataset that can be inspected and extended.

## Workflow

```text
Local literature archive
        |
        v
PDF text / Markdown extraction
        |
        v
Structured MOF extraction   (done upstream; not part of this package)
        |
        v
Schema normalization
        |
        v
Evidence validation
        |
        v
Versioned JSON dataset + validation report
```

The local literature archive is an input to the workflow, not part of the Git
repository.

## Data model

A normalized record is expected to contain the following top-level fields:

```json
{
  "MOF_name": "",
  "molecular_formula": "",
  "source_paper": "",
  "metal_node": {},
  "ligand": {},
  "topology": "",
  "Dimensionality": "",
  "Crystal_system": "",
  "Space_group": "",
  "properties": {},
  "characterization_data": {},
  "synthesis_method": "",
  "reaction_conditions": {},
  "raw_materials": "",
  "composition_structure": "",
  "application": ""
}
```

The current `normalize` step flattens accidentally nested arrays, strips legacy
`//error` markers while loading JSON, and rewrites each record with the expected
fields first (missing fields become `null`; unexpected fields are kept after them).
Standardizing naming conventions, distinguishing missing from genuinely unspecified
values, and moving validation errors into machine-readable metadata are planned.

## Validation approach

The `validate` command performs lexical evidence matching only:

1. Every document under `--papers` (`.md`, `.txt`, or `.pdf`) is read and split into
   overlapping chunks (1,500 characters by default, 150-character overlap).
2. Each non-empty string or numeric field of every record is normalized with
   Unicode NFKC, case folding, and whitespace collapsing. Chemical-formula variants
   and punctuation are not normalized further.
3. A field scores 1.0 when the normalized value occurs verbatim in a chunk;
   otherwise the score is the length of the longest common substring divided by the
   length of the value (Python `difflib`). Fields at or above `--threshold`
   (default 0.8) are reported as matched.

Two consequences matter when reading the report:

- All chunks from all supplied documents are pooled. A record is **not** restricted
  to the paper named in its `source_paper` field, so a value can be matched by text
  from a different paper. Pass only the relevant paper to `--papers` when checking a
  single record.
- Short values such as element symbols, single digits, or labels like `2D` match
  almost any text and carry little evidential weight.

The earlier prototype also experimented with a scientific-language transformer.
That dependency-heavy path is not enabled in the first cleaned release and will be
reintroduced only with reproducible model pinning and tests.

Automated matching can produce both false positives and false negatives. Chemical
formulae, crystallographic values, units, and numeric property values should receive
manual review before publication or downstream scientific use.

## Repository layout

```text
ecmof-pipeline/
├── src/ecmof_pipeline/
│   ├── __main__.py
│   ├── cli.py
│   ├── convert.py
│   ├── io.py
│   ├── literature.py
│   ├── normalize.py
│   ├── schema.py
│   └── validate.py
├── data/
│   ├── processed/
│   │   └── ecmof.json
│   └── samples/
├── schemas/
├── tests/
├── pyproject.toml
└── README.md
```

## Installation

Create an isolated environment and install the package in editable mode:

```bash
git clone https://github.com/ShunHao0626/ecmof-pipeline.git
cd ecmof-pipeline
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .          # core: no third-party dependencies
python -m pip install -e '.[pdf]'   # optional: PDF reading and conversion
```

The core package (normalization and validation of Markdown or text sources) uses
only the Python standard library. The optional `pdf` extra installs `pdfplumber`
(PDF text extraction during validation) and `pymupdf4llm` (the `convert` command).
No other conversion backend is currently supported.

## Command-line interface

```bash
# The installed console command `ecmof-pipeline` is equivalent to
# `python -m ecmof_pipeline`.

# Convert locally held papers to Markdown (requires the `pdf` extra).
python -m ecmof_pipeline convert \
  --input /path/to/local/papers \
  --output /path/to/local/markdown

# Normalize fragmented extraction files.
# --input may be repeated; each value can be a JSON file or a directory.
python -m ecmof_pipeline normalize \
  --input /path/to/local/raw-json \
  --output data/processed/ecmof.json

# Validate records against locally available source documents.
python -m ecmof_pipeline validate \
  --data data/processed/ecmof.json \
  --papers /path/to/local/papers \
  --report validation-report.json \
  --threshold 0.8 \
  --chunk-size 1500
```

## Data and copyright policy

This repository will not redistribute publisher PDFs, supplementary files, or
full-text Markdown copies unless their licenses explicitly permit redistribution.
Records should identify their source using DOI or another bibliographic reference
so that users can obtain the source through the appropriate publisher, repository,
or institutional access channel.

Only researcher-created annotations and small, legally redistributable examples
should be committed.

## Known limitations

- The draft dataset still contains inconsistent value types and naming styles.
- Some source fragments contain non-standard `//error` comments; `load_json`
  strips them automatically, but the flagged values still need manual review.
- Validation pools all supplied documents and does not check each record against
  its own `source_paper` (see [Validation approach](#validation-approach)).
- Lexical matching is evidence assistance, not scientific verification.
- The `processed/ecmof.json` snapshot has been flattened to 71 records but has not
  been deduplicated at DOI level (the records cite 21 distinct sources).
- Reproducibility depends on PDF text-extraction quality.

## Reproducibility

Public releases should record:

- Dataset version and checksum.
- Schema version.
- Matching thresholds.
- PDF extraction backend and version.
- Date of extraction and validation.

Generated caches, logs, model weights, private literature, and temporary conversion
outputs should remain outside Git or be ignored through `.gitignore`.

## Contributing

Contributions are welcome. Useful contributions
include schema discussions, validation tests, DOI corrections, extraction bug
reports, and manually verified records. Do not submit copyrighted article files.

## Citation

A versioned citation will be added with the first public dataset release. Until
then, cite the repository URL and the specific commit used in your work.

## License

No public license has been selected yet. Code and data licensing will be documented
separately before the first public release; third-party source documents are not
covered by the repository license.
