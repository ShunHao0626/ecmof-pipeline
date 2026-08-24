# EC-MOF Data Pipeline

> 中文简介：本项目用于整理电导型金属有机框架（electrically conductive
> metal-organic frameworks, EC-MOFs）文献，将论文转换为可处理文本，抽取
> MOF 结构、合成、表征和性能数据，并检查结构化记录是否得到原文支持。

EC-MOF Data Pipeline is a research-oriented workflow for building and validating
structured data about electrically conductive metal-organic frameworks. It brings
together literature organization, PDF-to-Markdown conversion, MOF record
normalization, and evidence-based validation.

The repository contains code and researcher-created structured data. Publisher
PDFs, supplementary documents, extracted figures, and full-text article copies
are intentionally excluded.

## Project status

This repository is the first cleaned release of an earlier research prototype. It
provides a small command-line interface, tests, a draft JSON schema, and a
mechanically repaired 71-record research snapshot. Scientific review of the data is
still in progress.

| Component | Status |
| --- | --- |
| Literature organization | Local workflow documented |
| PDF-to-Markdown conversion | Available as an optional feature |
| Structured MOF records | 71-record draft snapshot included |
| Exact and fuzzy validation | Available |
| Transformer-based semantic validation | Legacy prototype; not yet packaged |
| Command-line interface | Available |
| Automated tests | Included |

Results should be treated as research annotations rather than authoritative
chemical records until the validation status of each field has been reviewed.

## Goals

- Organize EC-MOF literature using stable identifiers such as DOI.
- Convert locally obtained papers into machine-readable text for private research.
- Represent structural, synthetic, characterization, and property information in
  a consistent JSON schema.
- Compare extracted values with source documents using exact, fuzzy, and semantic
  matching.
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
Structured MOF extraction
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

The cleanup process will standardize naming conventions, distinguish missing
values from genuinely unspecified values, flatten accidentally nested records,
and move validation errors into machine-readable metadata.

## Validation approach

The current prototype combines several forms of evidence checking:

1. Text normalization for punctuation, whitespace, and chemical formula variants.
2. Exact and fuzzy matching against chunks extracted from the source paper.
3. A configurable lexical threshold and explicit evidence report.

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
│   ├── literature.py
│   ├── convert.py
│   ├── normalize.py
│   ├── validate.py
│   └── cli.py
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
git clone <repository-url>
cd ecmof-pipeline
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Core validation currently depends on packages including `numpy`, `torch`,
`transformers`, `scipy`, `pdfplumber`, and fuzzy string-matching utilities.
PDF conversion has additional optional dependencies such as PyMuPDF, MinerU, or
`pymupdf4llm`.

## Command-line interface

```bash
# Convert locally held papers to Markdown.
python -m ecmof_pipeline convert \
  --input /path/to/local/papers \
  --output /path/to/local/markdown

# Normalize fragmented extraction files.
python -m ecmof_pipeline normalize \
  --input data/raw \
  --output data/processed/ecmof.json

# Validate records against locally available source documents.
python -m ecmof_pipeline validate \
  --data data/processed/ecmof.json \
  --papers /path/to/local/papers \
  --report validation-report.json
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
- Some source fragments contain non-standard `//error` comments and require repair.
- One draft aggregate contains an accidentally nested group of records.
- Model-based similarity is evidence assistance, not scientific verification.
- The original scripts contain platform-specific paths that must be removed.
- Reproducibility depends on model versions and PDF text-extraction quality.

## Reproducibility

Public releases should record:

- Dataset version and checksum.
- Schema version.
- Transformer model and revision.
- Matching thresholds.
- PDF extraction backend and version.
- Date of extraction and validation.

Generated caches, logs, model weights, private literature, and temporary conversion
outputs should remain outside Git or be ignored through `.gitignore`.

## Contributing

Contributions are welcome after the first cleaned release. Useful contributions
include schema discussions, validation tests, DOI corrections, extraction bug
reports, and manually verified records. Do not submit copyrighted article files.

## Citation

A versioned citation will be added with the first public dataset release. Until
then, cite the repository URL and the specific commit used in your work.

## License

No public license has been selected yet. Code and data licensing will be documented
separately before the first public release; third-party source documents are not
covered by the repository license.
