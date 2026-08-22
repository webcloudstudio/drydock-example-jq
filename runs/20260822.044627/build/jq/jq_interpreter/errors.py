"""Errors crossing the interpreter's process boundary."""


class CompileError(Exception):
    """The jq program could not be parsed or statically validated."""


class RuntimeError(Exception):
    """Evaluation failed after the program was compiled."""
