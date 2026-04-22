"""Cleaning utilities for the CSV processing pipeline."""

from __future__ import annotations

import re

import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names, replace spaces/special chars with underscores.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame(columns=["First Name", "Last-Name", "AGE"])
    >>> normalize_columns(df).columns.tolist()
    ['first_name', 'last_name', 'age']
    """
    df = df.copy()
    df.columns = [
        re.sub(r"[^a-z0-9]+", "_", col.strip().lower()).strip("_")
        for col in df.columns
    ]
    return df


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all string columns."""
    df = df.copy()
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda s: s.str.strip())
    return df


def drop_high_missing_columns(
    df: pd.DataFrame, threshold: float = 0.5
) -> pd.DataFrame:
    """Drop columns where the proportion of missing values ≥ *threshold*.

    Parameters
    ----------
    df:
        Input DataFrame.
    threshold:
        Fraction of missing values (0–1) above which a column is dropped.
        Default is 0.5 (50 %).

    Returns
    -------
    pd.DataFrame with offending columns removed.
    """
    if not 0 <= threshold <= 1:
        raise ValueError(f"threshold must be between 0 and 1, got {threshold}")
    missing_ratio = df.isnull().mean()
    keep = missing_ratio[missing_ratio < threshold].index
    dropped = [c for c in df.columns if c not in keep]
    if dropped:
        print(f"[cleaning] Dropped columns (>{threshold:.0%} missing): {dropped}")
    return df[keep].copy()


def fill_missing_numeric(
    df: pd.DataFrame, strategy: str = "median"
) -> pd.DataFrame:
    """Fill missing values in numeric columns with mean or median.

    Parameters
    ----------
    df:
        Input DataFrame.
    strategy:
        ``"mean"`` or ``"median"`` (default).

    Returns
    -------
    pd.DataFrame with numeric NaNs filled.
    """
    if strategy not in ("mean", "median"):
        raise ValueError(f"strategy must be 'mean' or 'median', got '{strategy}'")
    df = df.copy()
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        if df[col].isnull().any():
            fill_value = (
                df[col].mean() if strategy == "mean" else df[col].median()
            )
            df[col] = df[col].fillna(fill_value)
    return df


def fill_missing_categorical(df: pd.DataFrame, fill: str = "unknown") -> pd.DataFrame:
    """Fill missing values in object/string columns with *fill*."""
    df = df.copy()
    cat_cols = df.select_dtypes(include="object").columns
    df[cat_cols] = df[cat_cols].fillna(fill)
    return df


def clean(
    df: pd.DataFrame,
    *,
    drop_threshold: float = 0.5,
    numeric_strategy: str = "median",
) -> pd.DataFrame:
    """Run the full cleaning pipeline in order:

    1. normalize_columns
    2. strip_whitespace
    3. drop_high_missing_columns
    4. fill_missing_numeric
    5. fill_missing_categorical

    Returns a cleaned copy of *df*.
    """
    df = normalize_columns(df)
    df = strip_whitespace(df)
    df = drop_high_missing_columns(df, threshold=drop_threshold)
    df = fill_missing_numeric(df, strategy=numeric_strategy)
    df = fill_missing_categorical(df)
    return df
