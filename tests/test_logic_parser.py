import pytest
from logic_parser import token
from logic_parser.parser import Parser


# Tokenizer tests
def test_tokenize_simple_logic():
    stmt = "A ^ B"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
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
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert types == [token.TokenType.NOT, token.TokenType.IDENTIFIER]


def test_tokenize_or():
    stmt = "A v B"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.OR in types


def test_tokenize_implication():
    stmt = "A => B"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.IMPLICATION in types
    assert any(t.token == "=>" for t in tokens)


def test_tokenize_biconditional():
    stmt = "A <=> B"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.BICONDITIONAL in types
    assert any(t.token == "<=>" for t in tokens)


def test_tokenize_xor():
    stmt = "A != B"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.XOR in types
    assert any(t.token == "!=" for t in tokens)


# Parser and evaluation tests
def test_parse_and_eval_simple():
    stmt = "ABC := 1\nB := 0\nR := ABC ^ B\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_not():
    stmt = "A := 0\nR := ~A\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1 or result.eval() is True


def test_parse_and_eval_or():
    stmt = "A := 0\nB := 1\nR := A v B\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1


def test_parse_and_eval_precedence():
    stmt = "A := 1\nB := 0\nC := 1\nR := ~(A ^ B) v C\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1


def test_parse_and_eval_parentheses():
    stmt = "A := 1\nB := 0\nR := ~(A ^ (B v A))\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_implication():
    stmt = "A := 1\nB := 0\nR := A => B\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_biconditional():
    stmt = "A := 1\nB := 1\nR := A <=> B\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1

    stmt2 = "A := 1\nB := 0\nR := A <=> B\nR"
    tkz2 = token.Tokenizer(stmt2)
    tokens2 = tkz2.tokenize()
    parser2 = Parser(tokens2)
    result2 = parser2.parse()
    assert result2.eval() == 0


def test_parse_and_eval_xor():
    stmt = "A := 1\nB := 0\nR := A != B\nR"
    tkz = token.Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    assert result.eval() == 1

    stmt2 = "A := 1\nB := 1\nR := A != B\nR"
    tkz2 = token.Tokenizer(stmt2)
    tokens2 = tkz2.tokenize()
    parser2 = Parser(tokens2)
    result2 = parser2.parse()
    assert result2.eval() == 0


def test_invalid_token():
    stmt = "A = 1\nB = 0\nR = A $ B\nR"
    with pytest.raises(ValueError):
        tkz = token.Tokenizer(stmt)
        tokens = tkz.tokenize()
        parser = Parser(tokens)
        parser.parse()
