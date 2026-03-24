"""I/O helpers: read and write CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a CSV file into a DataFrame.

    Parameters
    ----------
    path:
        Path to the CSV file.
    **kwargs:
        Extra keyword arguments forwarded to :func:`pandas.read_csv`.

    Returns
    -------
    pd.DataFrame
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path, **kwargs)


def write_csv(df: pd.DataFrame, path: str | Path, **kwargs) -> None:
    """Write a DataFrame to a CSV file.

    Parameters
    ----------
    df:
        DataFrame to save.
    path:
        Destination path.
    **kwargs:
        Extra keyword arguments forwarded to :meth:`DataFrame.to_csv`.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    kwargs.setdefault("index", False)
    df.to_csv(path, **kwargs)
    print(f"[io] Saved {len(df):,} rows → {path}")


def print_summary(df: pd.DataFrame) -> None:
    """Print a short summary of a DataFrame to stdout."""
    print(f"\n{'='*50}")
    print(f"  Rows    : {len(df):,}")
    print(f"  Columns : {len(df.columns)}")
    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"  Missing : {total_missing:,} cells across {(missing > 0).sum()} columns")
    print(f"\n  Column types:\n{df.dtypes.to_string()}")
    print(f"\n  Basic stats:\n{df.describe(include='all').to_string()}")
    print("=" * 50)
