"""Tests for src.processing.cleaning."""

import pandas as pd
import pytest

from src.processing.cleaning import (
    clean,
    drop_high_missing_columns,
    fill_missing_categorical,
    fill_missing_numeric,
    normalize_columns,
    strip_whitespace,
)


# ---------------------------------------------------------------------------
# normalize_columns
# ---------------------------------------------------------------------------

def test_normalize_columns_lowercase():
    df = pd.DataFrame(columns=["First Name", "Last-Name", "AGE"])
    result = normalize_columns(df)
    assert result.columns.tolist() == ["first_name", "last_name", "age"]


def test_normalize_columns_special_chars():
    df = pd.DataFrame(columns=["col (1)", "col#2", "  spaces  "])
    result = normalize_columns(df)
    assert "col_1" in result.columns
    assert "col_2" in result.columns


def test_normalize_columns_does_not_mutate():
    df = pd.DataFrame(columns=["Hello World"])
    original_cols = df.columns.tolist()
    normalize_columns(df)
    assert df.columns.tolist() == original_cols


# ---------------------------------------------------------------------------
# strip_whitespace
# ---------------------------------------------------------------------------

def test_strip_whitespace():
    df = pd.DataFrame({"name": ["  Alice  ", " Bob"], "age": [30, 25]})
    result = strip_whitespace(df)
    assert result["name"].tolist() == ["Alice", "Bob"]
    assert result["age"].tolist() == [30, 25]


# ---------------------------------------------------------------------------
# drop_high_missing_columns
# ---------------------------------------------------------------------------

def test_drop_high_missing_columns_drops_above_threshold():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": [None, None, None, 4],  # 75 % missing
        }
    )
    result = drop_high_missing_columns(df, threshold=0.5)
    assert "a" in result.columns
    assert "b" not in result.columns


def test_drop_high_missing_columns_keeps_below_threshold():
    df = pd.DataFrame({"a": [1, None, 3], "b": [1, 2, 3]})
    result = drop_high_missing_columns(df, threshold=0.5)
    assert "a" in result.columns
    assert "b" in result.columns


def test_drop_high_missing_columns_invalid_threshold():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(ValueError):
        drop_high_missing_columns(df, threshold=1.5)


# ---------------------------------------------------------------------------
# fill_missing_numeric
# ---------------------------------------------------------------------------

def test_fill_missing_numeric_median():
    df = pd.DataFrame({"x": [1.0, 2.0, None, 4.0]})
    result = fill_missing_numeric(df, strategy="median")
    assert result["x"].isnull().sum() == 0
    assert result["x"].iloc[2] == pytest.approx(2.0)


def test_fill_missing_numeric_mean():
    df = pd.DataFrame({"x": [1.0, 3.0, None]})
    result = fill_missing_numeric(df, strategy="mean")
    assert result["x"].iloc[2] == pytest.approx(2.0)


def test_fill_missing_numeric_invalid_strategy():
    df = pd.DataFrame({"x": [1.0]})
    with pytest.raises(ValueError):
        fill_missing_numeric(df, strategy="mode")


# ---------------------------------------------------------------------------
# fill_missing_categorical
# ---------------------------------------------------------------------------

def test_fill_missing_categorical():
    df = pd.DataFrame({"dept": ["HR", None, "Eng"]})
    result = fill_missing_categorical(df, fill="unknown")
    assert result["dept"].tolist() == ["HR", "unknown", "Eng"]


# ---------------------------------------------------------------------------
# clean (integration)
# ---------------------------------------------------------------------------

def test_clean_pipeline():
    df = pd.DataFrame(
        {
            "First Name": ["  Alice  ", " Bob ", "Charlie"],
            "Score": [88.0, None, 92.0],
            "AllMissing": [None, None, None],
        }
    )
    result = clean(df, drop_threshold=0.9)
    assert "first_name" in result.columns
    assert "all_missing" not in result.columns
    assert result["score"].isnull().sum() == 0
    assert result["first_name"].str.contains(" ").sum() == 0
