"""Errors crossing the interpreter's process boundary."""


class CompileError(Exception):
    """The jq program could not be parsed or statically validated."""


class RuntimeError(Exception):
    """Evaluation failed after the program was compiled."""


class HaltError(Exception):
    """An intentional jq halt carrying the requested process exit status."""

    def __init__(self, value: object, exit_code: int) -> None:
        super().__init__(value)
        self.value = value
        self.exit_code = exit_code


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
