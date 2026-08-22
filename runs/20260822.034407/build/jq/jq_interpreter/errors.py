"""Errors and process-level status codes shared by interpreter boundaries."""

COMPILE_ERROR = 3
RUNTIME_ERROR = 5


class JqError(Exception):
    """Base class for errors that can be reported by the jq CLI."""


class CompileError(JqError):
    """The source program cannot be compiled."""


class RuntimeErrorJq(JqError):
    """A compiled filter failed while evaluating an input value."""
