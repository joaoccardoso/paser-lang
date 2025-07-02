from dataclasses import dataclass
import enum
from typing import Any, Optional


class TokenType(enum.Enum):
    WHITE_SPACE = enum.auto()
    COMMA = enum.auto()
    COLON = enum.auto()
    DOUBLE_QUOTES = enum.auto()
    OPEN_BRACKETS = enum.auto()
    CLOSE_BRACKETS = enum.auto()
    OPEN_CURLY_BRACKETS = enum.auto()
    CLOSE_CURLY_BRACKETS = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()
    TRUE = enum.auto()
    FALSE = enum.auto()
    NULL = enum.auto()


@dataclass
class Token:
    type: TokenType
    value: Optional[Any] = None


def tokenize(content: str, ignore_spaces: bool = True) -> list[Token]:
    tokens = []
    index = 0

    while index < len(content):
        c = content[index]
        match c:
            case "\t" | "\n" | " ":
                if not ignore_spaces:
                    tokens.append(Token(TokenType.WHITE_SPACE))
            case ",":
                tokens.append(Token(TokenType.COMMA))
            case ":":
                tokens.append(Token(TokenType.COLON))
            case '"':
                str_literal = ""
                index += 1
                start_index = index
                while index < len(content):
                    c = content[index]
                    if c != '"':
                        str_literal += c
                        index += 1
                    else:
                        break
                if index >= len(content) or content[index] != '"':
                    raise SyntaxError(
                        f"Unterminated string literal starting at position {start_index - 1}"
                    )
                tokens.append(Token(TokenType.STRING, str_literal))
            case "{":
                tokens.append(Token(TokenType.OPEN_CURLY_BRACKETS))
            case "}":
                tokens.append(Token(TokenType.CLOSE_CURLY_BRACKETS))
            case "[":
                tokens.append(Token(TokenType.OPEN_BRACKETS))
            case "]":
                tokens.append(Token(TokenType.CLOSE_BRACKETS))
            case _ if c.isdigit():
                numeric_literal = c
                index += 1
                has_dot = False
                while index < len(content):
                    c = content[index]
                    if c.isdigit():
                        numeric_literal += c
                        index += 1
                    elif c == ".":
                        if has_dot:
                            raise ValueError(
                                f"Invalid number format: multiple decimal points in '{numeric_literal + c}' at position {index}"
                            )
                        if index + 1 < len(content) and content[index + 1].isdigit():
                            numeric_literal += c
                            numeric_literal += content[index + 1]
                            index += 2
                            has_dot = True
                        else:
                            raise ValueError(
                                f"Invalid number format: decimal point not followed by digit at position {index}"
                            )
                    else:
                        break
                tokens.append(Token(TokenType.NUMBER, numeric_literal))
                continue  # index already advanced
            case "t":
                index = parse_literal(content, tokens, index, "true", TokenType.TRUE)
            case "f":
                index = parse_literal(content, tokens, index, "false", TokenType.FALSE)
            case "n":
                index = parse_literal(content, tokens, index, "null", TokenType.NULL)
            case _:
                raise SyntaxError(f"Unexpected character '{c}' at position {index}")
        index += 1

    return tokens


def parse_literal(
    content: str,
    tokens: list[Token],
    index: int,
    literal: str,
    expected_token: TokenType,
):
    lit_len = len(literal)
    if index + lit_len - 1 < len(content):
        value = content[index : index + lit_len]
        if value == literal:
            tokens.append(Token(expected_token))
            index += lit_len - 1
        else:
            raise ValueError(
                f"Unknown value '{value}' at position {index}, expected '{literal}'"
            )
    else:
        raise ValueError(
            f"Incomplete literal at position {index}, expected '{literal}'"
        )

    return index
