from dataclasses import dataclass
import enum
from typing import Any, Optional


RESERVED_SYMBOLS = ":()^~= \n\t"


class TokenType(enum.Enum):
    WHITE_SPACE = enum.auto()
    OPEN_P = enum.auto()
    CLOSE_P = enum.auto()
    IDENTIFIER = enum.auto()
    LITERAL = enum.auto()
    OR = enum.auto()
    AND = enum.auto()
    NOT = enum.auto()
    EQUAL = enum.auto()
    ASSIGN = enum.auto()


@dataclass
class Token:
    type: TokenType
    value: Optional[Any] = None


def tokenize(content: str) -> list[Token]:
    tokens = []
    i = 0
    while i < len(content):
        c = content[i]
        if c in "\n\t ":
            i += 1
            continue
        match c:
            case "~":
                tokens.append(Token(TokenType.NOT))
            case "^":
                tokens.append(Token(TokenType.AND))
            case "v":
                tokens.append(Token(TokenType.OR))
            case "(":
                tokens.append(Token(TokenType.OPEN_P))
            case ")":
                tokens.append(Token(TokenType.CLOSE_P))
            case "=":
                tokens.append(Token(TokenType.EQUAL))
            case "0" | "1":
                tokens.append(Token(TokenType.LITERAL, c))
            case ":":
                i += 1
                if i >= len(content):
                    raise ValueError("Unexpected end of file")
                c = content[i]
                if c == "=":
                    tokens.append(Token(TokenType.ASSIGN))
                else:
                    raise ValueError(f"Invalid Character: :{c}")

            case _ if c.isalpha():
                identifier = c
                i += 1
                while i < len(content):
                    c = content[i]
                    if c not in RESERVED_SYMBOLS:
                        identifier += c
                    else:
                        i -= 1
                        break
                    i += 1
                tokens.append(Token(TokenType.IDENTIFIER, identifier))
            case _:
                raise ValueError(f"Invalid Character: {c}")
        i += 1

    return tokens
