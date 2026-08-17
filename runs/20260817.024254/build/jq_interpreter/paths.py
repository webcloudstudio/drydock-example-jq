"""Reserved boundary for immutable path discovery and tree mutation."""

from .data_model import JsonValue


def replace_root(_value: JsonValue, replacement: JsonValue) -> JsonValue:
    """Return a replacement root without mutating the input tree."""
    return replacement
