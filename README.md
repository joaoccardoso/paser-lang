# json-parser

A simple JSON-like parser and tokenizer in Python.

## Features
- Tokenizes JSON-like input into tokens
- Parses tokens into Python data structures (dict, list, int, float, bool, None)
- Handles nested objects and arrays
- Provides clear error messages for invalid input

## Requirements
- Python 3.10+
- [pytest](https://pytest.org/) (for running tests)

## Installation

Install the package in editable mode with test dependencies:

```sh
pip install -e .[test]
```

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

### 2. Run the parser

```sh
python main.py
```

### 3. Run tests

```sh
pytest
```

## Project Structure

```
json_parser/
    token.py      # Tokenizer and token definitions
    parser.py     # Parser implementation
main.py          # Example usage
/tests/
    test_json_parser.py  # Pytest test cases
```

## Customization
- Edit or extend `json_parser/token.py` and `json_parser/parser.py` to support more features or custom syntax.

## License
MIT
