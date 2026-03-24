"""Tests for src.processing.features."""

import pandas as pd
import pytest

from src.processing.features import (
    add_missing_flag,
    add_row_id,
    encode_categorical,
    normalize_numeric,
)


def test_add_row_id_creates_column():
    df = pd.DataFrame({"a": [10, 20, 30]})
    result = add_row_id(df)
    assert "row_id" in result.columns
    assert result["row_id"].tolist() == [0, 1, 2]


def test_add_row_id_is_first_column():
    df = pd.DataFrame({"a": [1, 2]})
    result = add_row_id(df)
    assert result.columns[0] == "row_id"


def test_add_row_id_does_not_mutate():
    df = pd.DataFrame({"a": [1]})
    add_row_id(df)
    assert "row_id" not in df.columns


def test_add_missing_flag():
    df = pd.DataFrame({"x": [1.0, None, 3.0], "y": [4, 5, 6]})
    result = add_missing_flag(df, columns=["x"])
    assert "x_was_missing" in result.columns
    assert result["x_was_missing"].tolist() == [False, True, False]
    assert "y_was_missing" not in result.columns


def test_normalize_numeric_range():
    df = pd.DataFrame({"v": [0.0, 5.0, 10.0]})
    result = normalize_numeric(df)
    assert result["v"].min() == pytest.approx(0.0)
    assert result["v"].max() == pytest.approx(1.0)


def test_normalize_numeric_zero_variance():
    df = pd.DataFrame({"v": [3.0, 3.0, 3.0]})
    result = normalize_numeric(df)
    assert result["v"].tolist() == [3.0, 3.0, 3.0]


def test_encode_categorical():
    df = pd.DataFrame({"dept": ["HR", "Eng", "HR", "Marketing"]})
    result = encode_categorical(df, columns=["dept"])
    assert result["dept"].dtype.name in ("int8", "int16", "int32", "int64")
    assert len(result["dept"].unique()) == 3
