"""Ordered generator evaluator boundary."""

from .ast import Array, Comma, Filter, Identity, Limit, Literal, Raise
from .errors import RuntimeError
from .runtime import JsonValue, ValueStream, identity_stream


def evaluate(program: Filter, value: JsonValue) -> ValueStream:
    """Evaluate one input as an ordered stream of output values."""
    if isinstance(program, Identity):
        yield from identity_stream(value)
        return
    if isinstance(program, Literal):
        yield program.value
        return
    if isinstance(program, Comma):
        yield from evaluate(program.left, value)
        yield from evaluate(program.right, value)
        return
    if isinstance(program, Raise):
        raise RuntimeError(program.message)
    if isinstance(program, Array):
        yield list(evaluate(program.expression, value))
        return
    if isinstance(program, Limit):
        outputs = iter(evaluate(program.expression, value))
        for _ in range(program.count):
            try:
                yield next(outputs)
            except StopIteration:
                break
        return
    raise RuntimeError("unknown compiled filter")
