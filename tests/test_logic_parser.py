import pytest
from logic_parser import token
from logic_parser.parser import Parser


# Tokenizer tests
def test_tokenize_simple_logic():
    stmt = "A ^ B"
    tokens = token.tokenize(stmt)
    types = [t.type for t in tokens]
    assert types == [
        token.TokenType.IDENTIFIER,
        token.TokenType.AND,
        token.TokenType.IDENTIFIER,
    ]
    assert tokens[0].value == "A"
    assert tokens[2].value == "B"


def test_tokenize_not():
    stmt = "~A"
    tokens = token.tokenize(stmt)
    types = [t.type for t in tokens]
    assert types == [token.TokenType.NOT, token.TokenType.IDENTIFIER]


def test_tokenize_or():
    stmt = "A v B"
    tokens = token.tokenize(stmt)
    types = [t.type for t in tokens]
    assert token.TokenType.OR in types


# Parser and evaluation tests
def test_parse_and_eval_simple():
    stmt = "ABC := 1\nB := 0\nR := ABC ^ B\nR"
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_not():
    stmt = "A := 0\nR := ~A\nR"
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1 or result.eval() is True


def test_parse_and_eval_or():
    stmt = "A := 0\nB := 1\nR := A v B\nR"
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1


def test_parse_and_eval_precedence():
    stmt = "A := 1\nB := 0\nC := 1\nR := ~(A ^ B) v C\nR"
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1


def test_parse_and_eval_parentheses():
    stmt = "A = 1\nB = 0\nR = ~(A ^ (B v A))\nR"
    tokens = token.tokenize(stmt)
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 0


def test_invalid_token():
    stmt = "A = 1\nB = 0\nR = A $ B\nR"
    with pytest.raises(ValueError):
        tokens = token.tokenize(stmt)
        parser = Parser(tokens)
        parser.parse()
