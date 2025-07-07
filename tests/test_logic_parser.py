import pytest
from logic_parser import token
from logic_parser.exceptions import ParserError, TokenizerError
from logic_parser.expr import Expr
from logic_parser.parser import Parser
from logic_parser.tokenizer import Tokenizer


# Tokenizer tests
def test_tokenize_simple_logic():
    stmt = "A ^ B"
    tkz = Tokenizer(stmt)
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
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert types == [token.TokenType.NOT, token.TokenType.IDENTIFIER]


def test_tokenize_or():
    stmt = "A v B"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.OR in types


def test_tokenize_implication():
    stmt = "A => B"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.IMPLICATION in types
    assert any(t.token == "=>" for t in tokens)


def test_tokenize_biconditional():
    stmt = "A <=> B"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.BICONDITIONAL in types
    assert any(t.token == "<=>" for t in tokens)


def test_tokenize_xor():
    stmt = "A != B"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    types = [t.type for t in tokens]
    assert token.TokenType.XOR in types
    assert any(t.token == "!=" for t in tokens)


def test_tokenizer_line_and_line_pos():
    stmt = "A := 1\nB := 0\n  C := 1\n"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    # Check line and line_pos for some tokens
    a_token = tokens[0]
    assert a_token.token == "A"
    assert a_token.line == 1
    assert a_token.line_pos == 1
    b_token = next(t for t in tokens if t.token == "B")
    assert b_token.line == 2
    assert b_token.line_pos == 1
    c_token = next(t for t in tokens if t.token == "C")
    assert c_token.line == 3
    assert c_token.line_pos == 3  # two spaces before C


# Parser and evaluation tests
def test_parse_and_eval_simple():
    stmt = "ABC := 1\nB := 0\nR := ABC ^ B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_not():
    stmt = "A := 0\nR := ~A\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 1 or result.eval() is True


def test_parse_and_eval_or():
    stmt = "A := 0\nB := 1\nR := A v B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 1


def test_parse_and_eval_precedence():
    stmt = "A := 1\nB := 0\nC := 1\nR := ~(A ^ B) v C\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 1


def test_parse_and_eval_parentheses():
    stmt = "A := 1\nB := 0\nR := ~(A ^ (B v A))\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_implication():
    stmt = "A := 1\nB := 0\nR := A => B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 0


def test_parse_and_eval_biconditional():
    stmt = "A := 1\nB := 1\nR := A <=> B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 1

    stmt2 = "A := 1\nB := 0\nR := A <=> B\nR"
    tkz2 = Tokenizer(stmt2)
    tokens2 = tkz2.tokenize()
    parser2 = Parser(tokens2)
    result2 = parser2.parse()
    assert result2.eval() == 0


def test_parse_and_eval_xor():
    stmt = "A := 1\nB := 0\nR := A != B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 1

    stmt2 = "A := 1\nB := 1\nR := A != B\nR"
    tkz2 = Tokenizer(stmt2)
    tokens2 = tkz2.tokenize()
    parser2 = Parser(tokens2)
    result2 = parser2.parse()
    assert result2.eval() == 0


def test_invalid_token():
    stmt = "A = 1\nB = 0\nR = A $ B\nR"
    with pytest.raises(TokenizerError):
        tkz = Tokenizer(stmt)
        tokens = tkz.tokenize()
        parser = Parser(tokens, {})
        parser.parse()


def test_assignment_with_newline():
    stmt = "A := 1\nB := 0\nR := A ^ B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 0


def test_comment_only_line():
    stmt = "// this is a comment only line\nA := 1\nB := 0\nR := A v B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    result = parser.parse()
    assert result.eval() == 1


def test_assignment_without_newline_should_fail():
    stmt = "A := 1 B := 0\nR := A ^ B\nR"
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(ParserError):
        parser.parse()


def test_large_example():
    stmt = """
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
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    _ = parser.parse()

    assert_memory_entry(parser.memory["A"], True)
    assert_memory_entry(parser.memory["B"], False)
    assert_memory_entry(parser.memory["C"], True)
    assert_memory_entry(parser.memory["X"], False)
    assert_memory_entry(parser.memory["Y"], True)
    assert_memory_entry(parser.memory["Z"], True)
    assert_memory_entry(parser.memory["XOR1"], True)
    assert_memory_entry(parser.memory["XOR2"], True)
    assert_memory_entry(parser.memory["IMP1"], False)
    assert_memory_entry(parser.memory["IMP2"], True)
    assert_memory_entry(parser.memory["BIC1"], True)
    assert_memory_entry(parser.memory["BIC2"], False)

    assert "NESTED" in parser.memory
    assert "RESULT" in parser.memory


def test_parse_all_multiple_identifiers():
    stmt = """
    A := 1
    B := 0
    C := 1
    A
    B
    C
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    results = list(parser.parse_all())
    # The last three expressions are identifiers, so their eval should match the assignments
    assert results[-3].eval() is True  # A
    assert results[-2].eval() is False  # B
    assert results[-1].eval() is True  # C


def test_parse_all_with_comments_and_blank_lines():
    stmt = """
    // Assignments
    X := 1

    // Another assignment
    Y := 0

    // Now just identifiers
    X
    Y
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    results = list(parser.parse_all())
    # The last two expressions are identifiers
    assert results[-2].eval() is True  # X
    assert results[-1].eval() is False  # Y


def test_parser_error_line_and_line_pos():
    stmt = "A := 1\nB := 0\nC := 1\nD := 2\n"
    with pytest.raises(TokenizerError) as t_err:
        tkz = Tokenizer(stmt)
        tkz.tokenize()
    assert t_err.value.line == 4
    assert t_err.value.line_pos == 5


def assert_memory_entry(value: Expr | bool, expected_value: bool):
    if isinstance(value, Expr):
        assert value.eval() == expected_value
    else:
        assert value == expected_value


def test_function_definition_and_call():
    stmt = """
    NAND(x, y) := ~(x ^ y)
    A := 1
    B := 0
    R := NAND(A, B)
    R
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    results = list(parser.parse_all())
    # The last result is the function call R = NAND(A, B)
    assert results[-1].eval() is True
    # The function should be in the parser's function table
    assert "NAND" in parser.functions
    assert parser.functions["NAND"].args == ["x", "y"]


def test_function_wrong_arity():
    stmt = """
    NAND(x, y) := ~(x ^ y)
    A := 1
    R := NAND(A)
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(Exception) as excinfo:
        list(parser.parse_all())
    assert "arguments" in str(excinfo.value)


def test_function_nested_call():
    stmt = """
    NAND(x, y) := ~(x ^ y)
    NOR(x, y) := ~(x v y)
    A := 1
    C := 0
    R := NAND(NOR(A, C), C)
    R
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    results = list(parser.parse_all())
    assert results[-1].eval() is True


def test_function_call_undefined_function():
    stmt = """
    A := 1
    B := 0
    R := UNDEF(A, B)
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(Exception) as excinfo:
        list(parser.parse_all())
    assert "Function named 'UNDEF' not found" in str(excinfo.value)


def test_function_call_variable_as_function():
    stmt = """
    A := 1
    B := 0
    R := A(B)
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(ParserError) as excinfo:
        list(parser.parse_all())
    assert "Function named 'A' not found" in str(excinfo.value)


def test_function_call_too_many_args():
    stmt = """
    NAND(x, y) := ~(x ^ y)
    A := 1
    B := 0
    R := NAND(A, B, B)
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(Exception) as excinfo:
        list(parser.parse_all())
    assert "Expected 2 arguments for function 'NAND', got 3" in str(excinfo.value)


def test_function_call_too_few_args():
    stmt = """
    NAND(x, y) := ~(x ^ y)
    A := 1
    R := NAND(A)
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(Exception) as excinfo:
        list(parser.parse_all())
    assert "Expected 2 arguments for function 'NAND', got 1" in str(excinfo.value)


def test_function_call_non_identifier_arg():
    stmt = """
    NAND(x, y) := ~(x ^ y)
    R := NAND(B, 0)
    """
    tkz = Tokenizer(stmt)
    tokens = tkz.tokenize()
    parser = Parser(tokens, {})
    with pytest.raises(Exception) as excinfo:
        list(parser.parse_all())
    assert "No value found for variable name 'B'" in str(excinfo.value)
