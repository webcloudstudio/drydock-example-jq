"""Generator-valued evaluator for foundational jq expressions."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from jq_parser import Array, Comma, Field, Identity, Iterate, Literal, Pipe


class RuntimeErrorJq(Exception):
    pass


def evaluate(expression: Any, value: Any) -> Iterator[Any]:
    if isinstance(expression, Identity):
        yield value
    elif isinstance(expression, Literal):
        yield expression.value
    elif isinstance(expression, Field):
        if not isinstance(value, dict):
            raise RuntimeErrorJq("cannot index value")
        if expression.name in value:
            yield value[expression.name]
        else:
            yield None
    elif isinstance(expression, Iterate):
        if isinstance(value, list):
            yield from value
        elif isinstance(value, dict):
            yield from value.values()
        elif value is not None:
            raise RuntimeErrorJq("cannot iterate value")
    elif isinstance(expression, Pipe):
        for intermediate in evaluate(expression.left, value):
            yield from evaluate(expression.right, intermediate)
    elif isinstance(expression, Comma):
        yield from evaluate(expression.left, value)
        yield from evaluate(expression.right, value)
    elif isinstance(expression, Array):
        yield list(evaluate(expression.expression, value))
    else:
        raise RuntimeErrorJq("unknown expression")
