"""Path and update subsystem boundary.

Path operations are kept separate from filter evaluation so assignments and
deletion can share immutable traversal machinery in later blocks.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Path:
    """A JSON path represented by its ordered components."""

    components: tuple[str | int, ...] = ()

    def child(self, component: str | int) -> "Path":
        return Path(self.components + (component,))


def get_path(value: Any, path: Path) -> Any:
    """Read a path from a JSON value."""

    current = value
    for component in path.components:
        current = current[component]
    return current
