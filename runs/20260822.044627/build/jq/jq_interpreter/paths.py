"""Immutable path discovery and update boundary."""

from dataclasses import dataclass

from .runtime import JsonValue


@dataclass(frozen=True)
class Path:
    """A path into a JSON value, represented as immutable components."""

    components: tuple[str | int, ...] = ()


def get_path(value: JsonValue, path: Path) -> JsonValue:
    """Read a path without mutating the input value."""
    current = value
    for component in path.components:
        current = current[component]  # type: ignore[index]
    return current
