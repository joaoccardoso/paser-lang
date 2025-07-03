# Language Parser

A Python project with two main components:
- **json-parser**: A simple JSON-like parser and tokenizer.
- **logic-parser**: A parser and evaluator for propositional logic expressions.

---

## Features

### json-parser
- Tokenizes JSON-like input into tokens
- Parses tokens into Python data structures (`dict`, `list`, `int`, `float`, `bool`, `None`)
- Handles nested objects and arrays
- Provides clear error messages for invalid input

### logic-parser
- Tokenizes and parses propositional logic expressions (supports `~` (NOT), `^` (AND), `v` (OR), identifiers, parentheses)
- Evaluates logic expressions with variable assignment
- Supports operator precedence: NOT > AND > OR

---

## Requirements

- Python 3.10+
- [pytest](https://pytest.org/) (for running tests)

---

## Installation

Install the package in editable mode with test dependencies:

```sh
pip install -e .[test]
```

---

## Usage

### 1. Parse a JSON file

Example usage is provided in `main.py`:

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

Example usage for logic expressions:

```python
from logic_parser import token
from logic_parser.parser import Parser

def main():
    stmt = """
        A = 1
        B = 0
        C = 1
        R = ~(A^B)vC
        R
    """
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    print(f"Result: {result.eval()}")

if __name__ == "__main__":
    main()
```

---

## Running

### Run the JSON parser

```sh
python main.py
```

### Run tests

```sh
pytest
```

---

## Project Structure

```
json_parser/
    token.py      # JSON tokenizer and token definitions
    parser.py     # JSON parser implementation
logic_parser/
    token.py      # Logic tokenizer and token definitions
    parser.py     # Logic parser and evaluator
main.py          # Example usage
/tests/
    test_json_parser.py  # Pytest test cases for JSON parser
    test_logic_parser.py # Pytest test cases for logic parser
```

---

## Customization

- Edit or extend `json_parser/token.py`, `json_parser/parser.py`, `logic_parser/token.py`, and `logic_parser/parser.py` to support more features or custom syntax.

---

## License
MIT
