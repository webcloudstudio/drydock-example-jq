"""Builtin function registry boundary."""

from collections.abc import Callable
from typing import Any

Builtin = Callable[[Any], Any]


class BuiltinRegistry:
    """Name-to-builtin registry owned by the builtin subsystem."""

    def __init__(self) -> None:
        self._functions: dict[str, Builtin] = {}

    def register(self, name: str, function: Builtin) -> None:
        self._functions[name] = function

    def get(self, name: str) -> Builtin | None:
        return self._functions.get(name)
