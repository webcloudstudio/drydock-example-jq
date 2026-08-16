import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from jq_lexer import LexError, tokenize


def kinds(source: str) -> list[str]:
    return [token.kind for token in tokenize(source)]


def test_lexer_classifies_literals_fields_bindings_and_keywords():
    tokens = tokenize('42 .foo $value if .. @uri')
    assert [(token.kind, token.text) for token in tokens[:-1]] == [
        ("LITERAL", "42"),
        ("FIELD", "foo"),
        ("BINDING", "value"),
        ("if", "if"),
        ("..", ".."),
        ("FORMAT", "uri"),
    ]


def test_lexer_recognizes_longest_operators_in_source_order():
    assert kinds("!= == <= >= ?// //= |= += -= *= /= %= ..") == [
        "!=", "==", "<=", ">=", "?//", "//=", "|=", "+=", "-=", "*=", "/=", "%=", "..", "EOF",
    ]


def test_lexer_ignores_comments_but_not_comment_markers_in_strings():
    tokens = tokenize('"# text" # ignored\n 1')
    assert [token.text for token in tokens[:-1]] == ['"# text"', "1"]


def test_lexer_rejects_unterminated_strings_and_bad_escapes():
    with pytest.raises(LexError):
        tokenize('"unterminated')
    with pytest.raises(LexError):
        tokenize(r'"bad\q"')
