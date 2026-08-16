<!-- Compacted from builtin.jq sha256=b8a5fd9579be9b51c9a04e6620f8c1655539aa57eea33a84e202a8dea401f2a4 on 2026-08-16 by drydock build agent -->

Built-in contract surface: generator-aware filters include `map/1`, `select/1`, `sort_by/1`, `group_by/1`, `unique_by/1`, `max_by/1`, `min_by/1`, `add/0|1`, `recurse/0|1|2`, `while/2`, `until/2`, `limit/2`, `skip/2`, `first/0|1`, `last/0`, `nth/1|2`, `all/0|1|2`, `any/0|1|2`, `range/1|2|3`, `reduce`, and `foreach`. These consume and produce ordered jq streams, preserving backtracking and cartesian argument evaluation.

Collection/path interfaces include `map_values/1`, `del/1`, `getpath/1`, `setpath/2`, `delpaths/1`, `path/1`, `paths/0|1`, `pick/1`, `tostream`, `fromstream/1`, and `truncate_stream/1`. `empty` produces no values; `select` retains its input only for truthy results; assignment updates paths immutably.

Type/string/format interfaces include `type`, `length`, `keys`, `has`, `in`, `inside`, `join`, `split`, `splits`, `sub`, `gsub`, `match`, `test`, `capture`, `scan`, trimming/case functions, `tojson`, `fromjson`, `tostring`, and `@text|json|html|uri|urid|csv|tsv|sh|base64|base64d`.

Error/control interfaces include `error`, `try/catch`, `halt`, `halt_error`, labels/breaks, and optional `?`; runtime errors must preserve values emitted before failure. SQL-style interfaces include `INDEX`, `JOIN`, and `IN`.
