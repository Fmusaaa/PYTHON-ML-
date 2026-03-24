"""
Intermediate Python basics examples.

Topics covered:
  1. Type hints & typing module
  2. Dataclasses
  3. Generators & iterators
  4. List / dict comprehensions
  5. Error handling with custom exceptions
  6. Context managers
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generator, Iterator


# ---------------------------------------------------------------------------
# 1. Type hints
# ---------------------------------------------------------------------------

def greet(name: str, repeat: int = 1) -> str:
    """Return a greeting string, optionally repeated."""
    return (f"Hello, {name}! " * repeat).strip()


# ---------------------------------------------------------------------------
# 2. Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DataRecord:
    """A simple data record representing one row of a dataset."""

    id: int
    name: str
    value: float
    tags: list[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        """Return True if value is non-negative."""
        return self.value >= 0


# ---------------------------------------------------------------------------
# 3. Generators & iterators
# ---------------------------------------------------------------------------

def batch_rows(rows: list, batch_size: int = 10) -> Generator[list, None, None]:
    """Yield successive batches from *rows*."""
    for start in range(0, len(rows), batch_size):
        yield rows[start : start + batch_size]


def count_up(start: int, stop: int) -> Iterator[int]:
    """Simple counting generator."""
    current = start
    while current < stop:
        yield current
        current += 1


# ---------------------------------------------------------------------------
# 4. Comprehensions
# ---------------------------------------------------------------------------

def filter_positives(values: list[float]) -> list[float]:
    """Return only positive numbers using a list comprehension."""
    return [v for v in values if v > 0]


def square_map(values: list[float]) -> dict[float, float]:
    """Return a dict mapping value → value² using a dict comprehension."""
    return {v: v ** 2 for v in values}


# ---------------------------------------------------------------------------
# 5. Custom exceptions & error handling
# ---------------------------------------------------------------------------

class PipelineError(Exception):
    """Base exception for pipeline errors."""


class MissingColumnError(PipelineError):
    """Raised when a required column is absent from the DataFrame."""

    def __init__(self, column: str) -> None:
        self.column = column
        super().__init__(f"Required column '{column}' is missing from the dataset.")


def safe_divide(numerator: float, denominator: float) -> float:
    """Divide two numbers, raising ValueError on zero division."""
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


# ---------------------------------------------------------------------------
# 6. Context manager (using __enter__ / __exit__)
# ---------------------------------------------------------------------------

class Timer:
    """Simple wall-clock timer used as a context manager."""

    import time as _time

    def __enter__(self) -> "Timer":
        self._start = self._time.perf_counter()
        return self

    def __exit__(self, *_: object) -> None:
        self.elapsed = self._time.perf_counter() - self._start

    def __repr__(self) -> str:
        return f"Timer(elapsed={getattr(self, 'elapsed', None):.4f}s)"
