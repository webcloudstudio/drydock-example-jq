<!-- Compacted from parser.y sha256=803aa7c0b1acba2228e52d1de392fb51e60a7bbe23e42870aea1d62c43360c60 on 2026-08-16 by drydock build agent -->

Parser contract: jq supports identity `.`, literals, comma generators, field/index access, slices, arrays/objects, operators, conditionals, try/catch, reduce/foreach, bindings/patterns, functions, modules/imports, interpolation, formats, and assignments. Operator precedence is defined by the grammar; compile errors must be distinct from runtime errors. Module syntax must parse and reject invalid metadata without filesystem access.
