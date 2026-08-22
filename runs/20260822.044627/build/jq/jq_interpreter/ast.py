"""Syntax tree types shared by the lexer, parser, and evaluator."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Filter:
    """Base type for compiled jq filters."""


@dataclass(frozen=True)
class Identity(Filter):
    """The ``.`` filter, yielding its input unchanged."""


@dataclass(frozen=True)
class Iterate(Filter):
    """The ``.[]`` filter, yielding array or object members in order."""


@dataclass(frozen=True)
class Literal(Filter):
    """A JSON literal filter."""

    value: object


@dataclass(frozen=True)
class Comma(Filter):
    """Concatenate the output streams of two filters."""

    left: Filter
    right: Filter


@dataclass(frozen=True)
class Raise(Filter):
    """Raise a jq runtime error when evaluated."""

    message: str = "error"


@dataclass(frozen=True)
class Array(Filter):
    """Collect a filter's generated values into an array."""

    expression: Filter


@dataclass(frozen=True)
class Limit(Filter):
    """Keep at most ``count`` values from a filter stream."""

    count: int
    expression: Filter

@dataclass(frozen=True)
class Pipe(Filter):
    left: Filter
    right: Filter

@dataclass(frozen=True)
class StringTemplate(Filter):
    parts: tuple[str | Filter, ...]

@dataclass(frozen=True)
class Format(Filter):
    name: str
    template: StringTemplate | None = None

@dataclass(frozen=True)
class Add(Filter):
    left: Filter
    right: Filter

@dataclass(frozen=True)
class Node(Filter):
    """General expression node used by the complete source parser."""
    operation: str
    arguments: tuple[object, ...] = ()
