"""Generator-based jq evaluation boundary."""

from __future__ import annotations

import base64
import csv
import io
import json
import math
import time
from urllib.parse import quote, unquote

from jq_parser import Node


class RuntimeFailure(RuntimeError):
    """Raised after compilation when a filter cannot evaluate its input."""


def _json_safe(value: object) -> object:
    """Convert jq's non-finite numeric values to JSON's null representation."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    return value


def _json_text(value: object) -> str:
    return json.dumps(_json_safe(value), separators=(",", ":"), ensure_ascii=False)


def _text(value: object) -> str:
    return value if isinstance(value, str) else _json_text(value)


def _format(value: object, name: str) -> str:
    if name == "text":
        return _text(value)
    if name == "json":
        return _json_text(value)
    if name == "html":
        # Order matters: ampersands must be escaped first.
        return (_text(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace("'", "&apos;").replace('"', "&quot;"))
    if name == "uri":
        return quote(_text(value), safe="-._~")
    if name == "urid":
        return unquote(_text(value))
    if name == "base64":
        return base64.b64encode(_text(value).encode("utf-8")).decode("ascii")
    if name == "base64d":
        try:
            return base64.b64decode(_text(value), validate=True).decode("utf-8")
        except (ValueError, UnicodeDecodeError, base64.binascii.Error) as error:
            raise RuntimeFailure("invalid base64 input") from error
    if name in {"csv", "tsv"}:
        if not isinstance(value, list):
            raise RuntimeFailure(f"@{name} requires an array")
        fields = ["" if item is None else _text(item) for item in value]
        if name == "csv":
            output = io.StringIO()
            csv.writer(output, lineterminator="", quoting=csv.QUOTE_MINIMAL).writerow(fields)
            return output.getvalue()
        replacements = str.maketrans({"\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"})
        return "\t".join(field.translate(replacements) for field in fields)
    if name == "sh":
        values = value if isinstance(value, list) else [value]
        return " ".join("'" + _text(item).replace("'", "'\\''") + "'" for item in values)
    raise RuntimeFailure(f"unknown format @{name}")


def _index(key: object, source: object, optional: bool):
    try:
        if isinstance(source, dict) and isinstance(key, str):
            yield source.get(key)
        elif isinstance(source, list) and isinstance(key, (int, float)) and int(key) == key:
            index = int(key)
            yield source[index] if -len(source) <= index < len(source) else None
        elif isinstance(source, str) and isinstance(key, (int, float)) and int(key) == key:
            index = int(key)
            yield source[index] if -len(source) <= index < len(source) else None
        else:
            raise RuntimeFailure("cannot index value")
    except (IndexError, TypeError):
        if optional:
            yield None
        else:
            raise RuntimeFailure("cannot index value")


def _interpolated(node: Node, value: object, escape: str | None = None):
    results = [""]
    for part in node.children:
        rendered = []
        for item in _walk(part, value):
            rendered.append(_format(item, escape) if escape else _text(item))
        results = [prefix + suffix for prefix in results for suffix in rendered]
    yield from results


def _format_template(node: Node, value: object, name: str):
    results = [""]
    for part in node.children:
        if part.kind == "literal":
            rendered = [str(part.value)]
        else:
            rendered = [_format(item, name) for item in _walk(part, value)]
        results = [prefix + suffix for prefix in results for suffix in rendered]
    yield from results


def _call(node: Node, value: object):
    name = str(node.value)
    if name == "tostring":
        yield _text(value)
    elif name == "tojson":
        yield _json_text(value)
    elif name == "fromjson":
        try:
            yield json.loads(value)
        except (TypeError, json.JSONDecodeError) as error:
            raise RuntimeFailure("invalid JSON text") from error
    elif name == "type":
        yield ("null" if value is None else "boolean" if isinstance(value, bool)
               else "number" if isinstance(value, (int, float)) else "string" if isinstance(value, str)
               else "array" if isinstance(value, list) else "object")
    elif name == "length":
        if value is None:
            yield 0
        elif isinstance(value, (str, list, dict)):
            yield len(value)
        elif isinstance(value, (int, float)):
            yield abs(value)
        else:
            raise RuntimeFailure("length requires a string, array, object, or number")
    elif name == "contains" and len(node.children) == 1:
        needles = list(_walk(node.children[0], value))
        for needle in needles:
            if isinstance(value, str) and isinstance(needle, str):
                yield needle in value
            elif isinstance(value, list):
                yield all(item in value for item in needle) if isinstance(needle, list) else needle in value
            elif isinstance(value, dict) and isinstance(needle, dict):
                yield all(key in value and value[key] == item for key, item in needle.items())
            else:
                yield value == needle
    elif name == "strflocaltime" and len(node.children) == 1:
        for fmt in _walk(node.children[0], value):
            if not isinstance(fmt, str):
                raise RuntimeFailure("strflocaltime/1 requires a string format")
            yield time.strftime(fmt, time.localtime(value))
    else:
        raise RuntimeFailure(f"unknown builtin: {name}")


def _walk(node: Node, value: object):
    if node.kind == "identity":
        yield value
    elif node.kind == "literal":
        yield node.value
    elif node.kind == "true":
        yield True
    elif node.kind == "false":
        yield False
    elif node.kind == "null":
        yield None
    elif node.kind == "empty":
        return
    elif node.kind in {"string", "format_string"}:
        if node.kind == "string":
            yield from _interpolated(node, value)
        else:
            template, name = node.children[1], str(node.children[0].value)
            yield from _format_template(template, value, name)
    elif node.kind == "format":
        yield _format(value, str(node.value))
    elif node.kind == ",":
        yield from _walk(node.children[0], value)
        yield from _walk(node.children[1], value)
    elif node.kind == "|":
        for intermediate in _walk(node.children[0], value):
            yield from _walk(node.children[1], intermediate)
    elif node.kind in {"index", "index_opt"}:
        for source in _walk(node.children[0], value):
            key = node.value
            if key is None and len(node.children) > 1:
                for computed in _walk(node.children[1], source):
                    yield from _index(computed, source, node.kind == "index_opt")
            else:
                yield from _index(key, source, node.kind == "index_opt")
    elif node.kind == "array":
        items: list[object] = []
        for child in node.children:
            items.extend(_walk(child, value))
        yield items
    elif node.kind == "iterate":
        if isinstance(value, list):
            yield from value
        elif isinstance(value, dict):
            yield from value.values()
        else:
            raise RuntimeFailure("cannot iterate over this value")
    elif node.kind == "call":
        yield from _call(node, value)
    elif node.kind in {"+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="}:
        left = list(_walk(node.children[0], value))
        right = list(_walk(node.children[1], value))
        for first in left:
            for second in right:
                if node.kind == "+":
                    if first is None: result = second
                    elif second is None: result = first
                    elif isinstance(first, (int, float)) and isinstance(second, (int, float)): result = first + second
                    elif isinstance(first, str) and isinstance(second, str): result = first + second
                    elif isinstance(first, list) and isinstance(second, list): result = first + second
                    else: raise RuntimeFailure("cannot add values")
                elif node.kind == "-": result = first - second
                elif node.kind == "*": result = first * second
                elif node.kind == "/":
                    if second == 0: raise RuntimeFailure("division by zero")
                    result = first / second
                elif node.kind == "%": result = first % second
                elif node.kind == "==": result = first == second
                elif node.kind == "!=": result = first != second
                elif node.kind == "<": result = first < second
                elif node.kind == ">": result = first > second
                elif node.kind == "<=": result = first <= second
                else: result = first >= second
                yield result
    else:
        raise RuntimeFailure(f"unknown AST node: {node.kind}")


def evaluate(program: Node, value: object):
    """Evaluate an AST against one input, preserving ordered generator semantics."""
    yield from _walk(program, value)
