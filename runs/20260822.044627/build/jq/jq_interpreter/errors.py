"""Errors crossing the interpreter's process boundary."""


class CompileError(Exception):
    """The jq program could not be parsed or statically validated."""


class RuntimeError(Exception):
    """Evaluation failed after the program was compiled."""


# Runtime failures raised by evaluator helpers must have the same semantics as
# jq errors when they cross a flow operator.  Keep this tuple shared by the
# evaluator and the CLI so try/optional do not accidentally miss a Python
# arithmetic or recursion failure.
FLOW_RUNTIME_ERRORS = (
    RuntimeError,
    ValueError,
    TypeError,
    IndexError,
    ArithmeticError,
    RecursionError,
)
