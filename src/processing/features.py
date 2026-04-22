"""Simple feature engineering for the CSV processing pipeline."""

from __future__ import annotations

import pandas as pd


def add_row_id(df: pd.DataFrame, column_name: str = "row_id") -> pd.DataFrame:
    """Add a zero-based integer row-ID column as the first column."""
    df = df.copy()
    df.insert(0, column_name, range(len(df)))
    return df


def add_missing_flag(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Add a boolean ``<col>_was_missing`` flag for each column that had NaNs.

    Parameters
    ----------
    df:
        Input DataFrame (should be called *before* filling missing values).
    columns:
        Columns to check. If *None*, checks all columns.
    """
    df = df.copy()
    cols = columns if columns is not None else df.columns.tolist()
    for col in cols:
        if col in df.columns and df[col].isnull().any():
            df[f"{col}_was_missing"] = df[col].isnull()
    return df


def normalize_numeric(
    df: pd.DataFrame, columns: list[str] | None = None
) -> pd.DataFrame:
    """Min-max scale numeric columns to the [0, 1] range.

    Columns with zero variance are left unchanged.
    """
    df = df.copy()
    num_cols = (
        columns
        if columns is not None
        else df.select_dtypes(include="number").columns.tolist()
    )
    for col in num_cols:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max != col_min:
            df[col] = (df[col] - col_min) / (col_max - col_min)
    return df


def encode_categorical(
    df: pd.DataFrame, columns: list[str] | None = None
) -> pd.DataFrame:
    """Encode object columns as integer category codes.

    The original column is replaced with its integer code (0-based).
    A ``<col>_label`` column is NOT added to keep things simple.
    """
    df = df.copy()
    cat_cols = (
        columns
        if columns is not None
        else df.select_dtypes(include="object").columns.tolist()
    )
    for col in cat_cols:
        df[col] = df[col].astype("category").cat.codes
    return df
