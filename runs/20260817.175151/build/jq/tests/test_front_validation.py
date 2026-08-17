import io

import jq


def compile_status(program: str) -> tuple[int, str]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO("null\n"), output)
    return status, output.getvalue()


def test_unterminated_program_is_rejected_before_evaluation() -> None:
    assert compile_status("{") == (3, "")


def test_undefined_binding_is_rejected_before_evaluation() -> None:
    assert compile_status(". as $known | $unknown") == (3, "")


def test_constant_non_string_object_key_is_rejected() -> None:
    assert compile_status("{(0):1}") == (3, "")


def test_unresolved_break_label_is_rejected() -> None:
    assert compile_status(". as $foo | break $foo") == (3, "")


def test_valid_program_reaches_evaluation() -> None:
    output = io.StringIO()
    status = jq.run(["-c", "."], io.StringIO('{"valid":[1,2]}\n'), output)
    assert status == 0
    assert output.getvalue() == '{"valid":[1,2]}\n'
