import pytest

from jq_interpreter.diagnostics import CompileError
from jq_interpreter.lexer import tokenize


def kinds(program: str) -> list[str]:
    return [token.kind for token in tokenize(program)]


def test_lexer_recognizes_fields_bindings_formats_and_operators() -> None:
    tokens = tokenize('.name $value @base64 ?// //= ..')
    assert [(token.kind, token.value) for token in tokens[:-1]] == [
        ('FIELD', 'name'), ('BINDING', 'value'), ('FORMAT', 'base64'),
        ('?//', '?//'), ('//=', '//='), ('..', '..'),
    ]


def test_lexer_decodes_json_escapes_and_retains_location() -> None:
    token = tokenize('\n  "a\\n\\u0042"')[0]
    assert token.kind == 'STRING'
    assert token.value == 'a\nB'
    assert (token.line, token.column) == (2, 3)


def test_lexer_preserves_interpolation_as_expression_source() -> None:
    token = tokenize('"prefix-\\(.name)"')[0]
    assert token.value == [('text', 'prefix-'), ('expr', '.name')]


@pytest.mark.parametrize('program', ['"bad\\q"', '"bad\\u12"', '[', '{', '(]'])
def test_lexer_rejects_invalid_escapes_and_delimiters(program: str) -> None:
    with pytest.raises(CompileError):
        tokenize(program)


def test_lexer_ignores_comments_and_escaped_line_continuations() -> None:
    assert kinds('# comment\\\n . # trailing\n | 1') == ['|', 'NUMBER', 'EOF']
