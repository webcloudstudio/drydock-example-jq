<!-- Compacted from lexer.l sha256=cfb3af17a786df30d7e30dae5861b84747d4904f8ce7ae9ab9b48bde342ee7f3 on 2026-08-16 by drydock build agent -->

Lexer contract: recognize jq keywords, identifiers, bindings, fields, literals, formats, comments, operators, delimiters, recursive descent, strings with JSON escapes, and string interpolation. Preserve source locations and reject invalid characters or malformed literals during compilation.
