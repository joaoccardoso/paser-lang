# Parser Lang

A Python project with two main components:
- **json-parser**: A simple JSON-like parser and tokenizer.
- **logic-parser**: A parser and evaluator for propositional logic expressions.

## Features

### json_parser
- Tokenizes JSON-like input into tokens
- Parses tokens into Python data structures (`dict`, `list`, `int`, `float`, `bool`, `None`)
- Handles nested objects and arrays
- Provides clear error messages for invalid input

### logic_parser
- Tokenizes and parses propositional logic expressions (supports `~` (NOT), `^` (AND), `v` (OR), `!=` (XOR), `=>` (IMPLICATION), `<=>` (BICONDITIONAL), identifiers, parentheses)
- Evaluates logic expressions with variable assignment (`:=`)
- Supports operator precedence: `NOT` > `AND` > `XOR` > `OR` > `IMPLICATION` > `BICONDITIONAL`
- Includes an interactive REPL for logic expressions
- Can run logic files directly from the command line

## Requirements

- Python 3.10+
- [pytest](https://pytest.org/) (for running tests)

## Installation

Install the package in editable mode and the test dependencies using `requirements.txt`:

```sh
pip install -r requirements.txt
```

## Usage

### 1. Parse a JSON file

```python
from pathlib import Path
from pprint import pprint
from json_parser.parser import Parser
from json_parser.token import tokenize

def main():
    file = Path("./data.json")
    with file.open() as f:
        content = f.read()
    tokens = tokenize(content, ignore_spaces=True)
    parser = Parser(tokens)
    result = parser.parse()
    pprint(result)

if __name__ == "__main__":
    main()
```

### 2. Parse and evaluate a logic expression

```python
from logic_parser import token
from logic_parser.parser import Parser

def main():
    stmt = """
        A := 1
        B := 0
        C := 1
        R := ~(A^B)vC
        R
    """
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    print(f"Result: {result.eval()}")

if __name__ == "__main__":
    main()
```

### 3. Run the Logic REPL or a Logic File

You can interactively evaluate logic expressions using the REPL, or run a file with logic expressions:

```sh
python -m logic_parser.main [file]
```
- If `[file]` is provided, the program will evaluate the file and print the result of the last expression.
- If no file is provided, the interactive REPL will start.
- Use `-h` to show usage instructions.

Example REPL session:
```
Positional Logic REPL
?> A := 1
?> B := 0
?> R := (A ^ B) => ~(A v B)
?> R
True
```
Press Ctrl+C to exit the REPL.

### 4. Large Example

You can use a large example to test all features at once:

```c
// Variable assignments
A := 1
B := 0
C := 1

// Simple AND, OR, NOT
X := A ^ B
Y := ~B
Z := A v B

// XOR, IMPLICATION, BICONDITIONAL
XOR1 := A != B
XOR2 := B != C
IMP1 := A => B
IMP2 := B => C
BIC1 := A <=> C
BIC2 := A <=> B

// Nested expressions and parentheses
NESTED := ~(A ^ (B v C)) => ((A != B) <=> (C ^ 1))

// Comments and blank lines
// The next line checks a complex formula
RESULT := (A ^ ~B) v ((A => C) <=> (B != C))

// Print results
A
B
C
X
Y
Z
XOR1
XOR2
IMP1
IMP2
BIC1
BIC2
NESTED
RESULT
```

## Running tests

```sh
pytest
```

## Project Structure

```
json_parser/
    token.py      # JSON tokenizer and token definitions
    parser.py     # JSON parser implementation
logic_parser/
    token.py      # Logic tokenizer and token definitions
    parser.py     # Logic parser and evaluator
    repl.py       # Interactive REPL for logic expressions
    main.py       # Entry point for REPL and file execution
/tests/
    test_json_parser.py  # Pytest test cases for JSON parser
    test_logic_parser.py # Pytest test cases for logic parser
```

## License

MIT
