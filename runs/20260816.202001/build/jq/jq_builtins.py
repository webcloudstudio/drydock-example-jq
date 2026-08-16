"""Registry boundary for standard-library jq builtin filters.

The full builtin surface is implemented incrementally by later build blocks; keeping
registration here prevents the runtime from depending on CLI or parser details.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any


Builtin = Callable[[Any], Iterator[Any]]


def _identity(value: Any) -> Iterator[Any]:
    yield value


BUILTINS: dict[str, Builtin] = {"identity": _identity}


def get_builtin(name: str) -> Builtin:
    """Return a registered builtin or raise a lookup error."""
    try:
        return BUILTINS[name]
    except KeyError as error:
        raise KeyError(f"unknown builtin: {name}") from error
