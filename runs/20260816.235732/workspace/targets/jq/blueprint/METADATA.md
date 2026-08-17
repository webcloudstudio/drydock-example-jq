# jq Interpreter

display_name: jq Interpreter
short_description: A standalone Python interpreter for the jq language that reads JSON from stdin and emits filtered JSON values.
status: active
stack: Python 3.11+ standard library; POSIX sh
code_root: .
project_shape: cli
executable: ./jq
input: JSON values from stdin
output: compact JSON values on stdout
compile_exit_code: 3
runtime_exit_code: 5
verification: sh sources/full_test.sh
runtime_dependencies: none
