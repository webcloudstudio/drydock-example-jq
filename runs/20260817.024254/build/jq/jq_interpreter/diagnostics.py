"""Typed failures shared by compilation and execution boundaries."""


class CompileError(Exception):
    """The program is syntactically or statically invalid."""


class RuntimeJqError(Exception):
    """The program compiled but failed while processing a value."""
