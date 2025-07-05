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

### 3. Run the Logic REPL

You can interactively evaluate logic expressions using the REPL:

```sh
python -m logic_parser.main
```

Example session:
```
Positional Logic REPL
?> A := 1
?> B := 0
?> R := (A ^ B) => ~(A v B)
?> R
True
```
Press Ctrl+C to exit the REPL.

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
    main.py       # Entry point for REPL
/tests/
    test_json_parser.py  # Pytest test cases for JSON parser
    test_logic_parser.py # Pytest test cases for logic parser
```

## License

MIT
