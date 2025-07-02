import pytest
from json_parser.token import tokenize, TokenType
from json_parser.parser import Parser


# Tokenizer tests
def test_tokenize_simple_object():
    content = '{"a": 1, "b": 2}'
    tokens = tokenize(content, ignore_spaces=True)
    types = [t.type for t in tokens]
    assert types == [
        TokenType.OPEN_CURLY_BRACKETS,
        TokenType.STRING,
        TokenType.COLON,
        TokenType.NUMBER,
        TokenType.COMMA,
        TokenType.STRING,
        TokenType.COLON,
        TokenType.NUMBER,
        TokenType.CLOSE_CURLY_BRACKETS,
    ]
    assert tokens[1].value == "a"
    assert tokens[5].value == "b"
    assert tokens[3].value == "1"
    assert tokens[7].value == "2"


def test_tokenize_literals():
    content = '{"t": true, "f": false, "n": null}'
    tokens = tokenize(content, ignore_spaces=True)
    types = [t.type for t in tokens]
    assert TokenType.TRUE in types
    assert TokenType.FALSE in types
    assert TokenType.NULL in types


# Parser tests
def test_parse_simple_object():
    content = '{"x": 42}'
    tokens = tokenize(content, ignore_spaces=True)
    parser = Parser(tokens)
    result = parser.parse()
    assert result == {"x": 42}


def test_parse_nested_object():
    content = '{"a": {"b": [1, 2, 3]}}'
    tokens = tokenize(content, ignore_spaces=True)
    parser = Parser(tokens)
    result = parser.parse()
    assert result == {"a": {"b": [1, 2, 3]}}


def test_parse_array():
    content = "[10, 20, 30]"
    tokens = tokenize(content, ignore_spaces=True)
    parser = Parser(tokens)
    result = parser.parse()
    assert result == [10, 20, 30]


def test_parse_literals():
    content = '{"t": true, "f": false, "n": null}'
    tokens = tokenize(content, ignore_spaces=True)
    parser = Parser(tokens)
    result = parser.parse()
    assert isinstance(result, dict)
    assert result.get("t") is True
    assert result.get("f") is False
    assert result.get("n") is None


def test_tokenize_invalid_character():
    with pytest.raises(SyntaxError):
        tokenize('{"a"=1}', ignore_spaces=True)


def test_tokenize_unterminated_string():
    with pytest.raises(SyntaxError):
        tokenize('{"a: 1}', ignore_spaces=True)
