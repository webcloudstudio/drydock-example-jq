import pytest

from jq_interpreter.errors import CompileError
from jq_interpreter.lexer import TokenKind, tokenize


def test_scans_literals_keywords_and_operators_in_source_order() -> None:
    tokens = tokenize('def f($x): .foo == 1; $x // null')
    assert [token.kind for token in tokens[:-1]] == [
        TokenKind.KEYWORD, TokenKind.IDENTIFIER, TokenKind.DELIMITER,
        TokenKind.BINDING, TokenKind.DELIMITER, TokenKind.DELIMITER,
        TokenKind.FIELD, TokenKind.OPERATOR, TokenKind.NUMBER,
        TokenKind.DELIMITER, TokenKind.BINDING, TokenKind.OPERATOR,
        TokenKind.IDENTIFIER,
    ]
    assert [token.position for token in tokens[:3]] == [0, 4, 5]
    assert tokens[-1].kind is TokenKind.END


def test_scans_comments_and_json_string_escapes() -> None:
    tokens = tokenize('1 # ignored\n "a\\n#b"')
    assert [token.text for token in tokens[:-1]] == ["1", '"', r"a\n#b", '"']


def test_scans_formats_and_qualified_bindings() -> None:
    tokens = tokenize('@json $module::value .field')
    assert [(token.kind, token.text) for token in tokens[:-1]] == [
        (TokenKind.FORMAT, "@json"),
        (TokenKind.BINDING, "$module::value"),
        (TokenKind.FIELD, ".field"),
    ]


@pytest.mark.parametrize("source", ['"bad\\q"', '"unterminated'])
def test_rejects_invalid_lexical_source(source: str) -> None:
    with pytest.raises(CompileError):
        tokenize(source)
