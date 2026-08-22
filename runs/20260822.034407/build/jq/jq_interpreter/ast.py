"""Small, immutable syntax tree types shared by the parser and evaluator."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SourceLocation:
    """A one-based source position used in diagnostics."""

    line: int
    column: int


@dataclass(frozen=True)
class Filter:
    """Base type for compiled jq filters."""


@dataclass(frozen=True)
class Identity(Filter):
    """The identity filter, represented explicitly in the AST."""


@dataclass(frozen=True)
class Literal(Filter):
    """A JSON-compatible literal value."""

    value: Any


@dataclass(frozen=True)
class Pipeline(Filter):
    """A left-to-right filter pipeline."""

    left: Filter
    right: Filter


@dataclass(frozen=True)
class Comma(Filter):
    """A concatenation of two generator streams."""

    left: Filter
    right: Filter
