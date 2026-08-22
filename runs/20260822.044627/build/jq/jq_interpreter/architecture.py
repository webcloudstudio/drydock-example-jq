"""Stable ownership map for the standalone interpreter.

This module contains only architectural metadata and process-level constants.
Feature implementations belong in the modules named by ``MODULE_BOUNDARIES``.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleBoundary:
    """Name and responsibility of one interpreter subsystem."""

    module: str
    responsibility: str


MODULE_BOUNDARIES: tuple[ModuleBoundary, ...] = (
    ModuleBoundary("jq", "executable entry point and command-line validation"),
    ModuleBoundary("jq_interpreter.lexer", "source text to positioned tokens"),
    ModuleBoundary("jq_interpreter.parser", "tokens to immutable filter AST"),
    ModuleBoundary("jq_interpreter.ast", "immutable syntax and compiled filter nodes"),
    ModuleBoundary("jq_interpreter.evaluator", "ordered generator evaluation and control flow"),
    ModuleBoundary("jq_interpreter.runtime", "JSON values, streams, and evaluation context"),
    ModuleBoundary("jq_interpreter.paths", "immutable path reads and updates"),
    ModuleBoundary("jq_interpreter.builtins", "jq standard-library filter implementations"),
    ModuleBoundary("jq_interpreter.diagnostics", "diagnostics and process exit policy"),
)

COMPILE_EXIT = 3
RUNTIME_EXIT = 5
