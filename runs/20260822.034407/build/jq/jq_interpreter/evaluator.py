"""Ordered generator evaluation boundary."""

from collections.abc import Iterator
from typing import Any

from .ast import Comma, Filter, Identity, Literal, Pipeline
from .errors import RuntimeErrorJq


def evaluate(program: Filter, input_value: Any) -> Iterator[Any]:
    """Yield every output in jq order, preserving stream multiplicity."""

    if isinstance(program, Identity):
        yield input_value
    elif isinstance(program, Literal):
        yield program.value
    elif isinstance(program, Comma):
        yield from evaluate(program.left, input_value)
        yield from evaluate(program.right, input_value)
    elif isinstance(program, Pipeline):
        for intermediate in evaluate(program.left, input_value):
            yield from evaluate(program.right, intermediate)
    else:
        raise RuntimeErrorJq("unknown filter")
