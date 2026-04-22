"""CLI entry point for the CSV processing pipeline.

Usage
-----
python -m src.processing.run --input data/raw/sample.csv --output data/processed/sample_clean.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.processing.cleaning import clean
from src.processing.features import add_row_id
from src.processing.io import print_summary, read_csv, write_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-pipeline",
        description="Read → Clean → Feature-engineer → Write a CSV file.",
    )
    parser.add_argument(
        "--input",
        default="data/raw/sample.csv",
        help="Path to input CSV file (default: data/raw/sample.csv)",
    )
    parser.add_argument(
        "--output",
        default="data/processed/output.csv",
        help="Path to write processed CSV (default: data/processed/output.csv)",
    )
    parser.add_argument(
        "--drop-threshold",
        type=float,
        default=0.5,
        dest="drop_threshold",
        help="Drop columns where missing fraction >= this value (default: 0.5)",
    )
    return parser


def run_pipeline(
    input_path: str,
    output_path: str,
    drop_threshold: float = 0.5,
) -> None:
    """Execute the full pipeline programmatically."""
    print(f"\n[pipeline] Reading  : {input_path}")
    df_raw = read_csv(input_path)

    print("\n--- RAW DATA SUMMARY ---")
    print_summary(df_raw)

    print("\n[pipeline] Cleaning ...")
    df_clean = clean(df_raw, drop_threshold=drop_threshold)

    print("\n[pipeline] Adding features ...")
    df_out = add_row_id(df_clean)

    print("\n--- PROCESSED DATA SUMMARY ---")
    print_summary(df_out)

    write_csv(df_out, output_path)
    print(f"\n[pipeline] Done. Output → {Path(output_path).resolve()}")


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    run_pipeline(
        input_path=args.input,
        output_path=args.output,
        drop_threshold=args.drop_threshold,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
