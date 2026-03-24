# Python Basics + CSV Data Processing Pipeline

> **Intermediate-level** project for learning Python fundamentals alongside a real CSV data-processing pipeline.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Install Dependencies](#install-dependencies)
5. [Running Notebooks](#running-notebooks)
6. [Running the CLI Pipeline](#running-the-cli-pipeline)
7. [Repository Structure](#repository-structure)
8. [Example Commands](#example-commands)

---

## Project Overview

This repository combines:
- **Python Basics** – intermediate examples covering generators, dataclasses, typing, comprehensions, and error handling.
- **CSV Data Processing Pipeline** – a modular pipeline that reads a raw CSV, cleans it, engineers features, and writes a processed CSV.

Originally the repo only contained Jupyter Notebooks. This structure keeps those notebooks but adds proper Python modules so the project can be run as a standalone pipeline.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | ≥ 3.9 |
| pip | ≥ 22 |

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Fmusaaa/PYTHON-ML-.git
cd PYTHON-ML-

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

To install the project as an editable package (so `src.*` imports work everywhere):
```bash
pip install -e .
```

---

## Running Notebooks

```bash
jupyter notebook
```

Open `notebooks/01_csv_pipeline_demo.ipynb` to see an end-to-end walkthrough.

---

## Running the CLI Pipeline

```bash
python -m src.processing.run \
    --input  data/raw/sample.csv \
    --output data/processed/sample_clean.csv
```

**Options**

| Flag | Description | Default |
|------|-------------|---------|
| `--input` | Path to input CSV | `data/raw/sample.csv` |
| `--output` | Path to save processed CSV | `data/processed/output.csv` |
| `--drop-threshold` | Drop columns where missing % ≥ this value (0–1) | `0.5` |

---

## Repository Structure

```
PYTHON-ML-/
├── data/
│   ├── raw/
│   │   └── sample.csv          # Tiny synthetic dataset
│   └── processed/              # Pipeline output (git-ignored)
├── notebooks/
│   └── 01_csv_pipeline_demo.ipynb
├── src/
│   ├── __init__.py
│   ├── basic/
│   │   ├── __init__.py
│   │   └── examples.py         # Generators, dataclasses, typing, etc.
│   └── processing/
│       ├── __init__.py
│       ├── io.py               # read_csv / write_csv helpers
│       ├── cleaning.py         # Missing-value handling, column normalisation
│       ├── features.py         # Simple feature engineering
│       └── run.py              # CLI entry point (argparse)
├── tests/
│   ├── test_cleaning.py
│   └── test_features.py
├── WINE-QUALITY(DATA PROCESING)/
│   └── WINE_QUALITY.ipynb      # Original notebook (kept)
├── lat-heart/
│   └── Latihan_pert1.ipynb     # Original notebook (kept)
├── .gitignore
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Example Commands

```bash
# Run the pipeline on the sample data
python -m src.processing.run --input data/raw/sample.csv --output data/processed/sample_clean.csv

# Run tests
pytest tests/ -v

# Make shortcuts
make run        # runs pipeline on sample data
make test       # runs pytest
make lint       # runs ruff (if installed)
```

---

## Original Notebooks

The original notebooks are preserved in their folders:

- `WINE-QUALITY(DATA PROCESING)/WINE_QUALITY.ipynb` – Wine Quality EDA & ML
- `lat-heart/Latihan_pert1.ipynb` – Heart Disease dataset exploration
