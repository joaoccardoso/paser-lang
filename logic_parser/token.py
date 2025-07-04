from dataclasses import dataclass
import enum
from typing import Any, Optional


RESERVED_SYMBOLS = ":()^~= \n\t"


class TokenType(enum.Enum):
    WHITESPACE = enum.auto()
    OPEN_P = enum.auto()
    CLOSE_P = enum.auto()
    IDENTIFIER = enum.auto()
    LITERAL = enum.auto()
    OR = enum.auto()
    AND = enum.auto()
    NOT = enum.auto()
    EQUAL = enum.auto()
    ASSIGN = enum.auto()
    COLON = enum.auto()


@dataclass
class Token:
    token: str
    type: TokenType
    value: Optional[Any] = None


class Tokenizer:
    def __init__(self, content: str) -> None:
        self.content = content
        self.tokens = []
        self.pos = 0

    def peek(self, next: int = 0):
        if self.pos + next < len(self.content):
            return self.content[self.pos + next]
        return None

    def consume(self, expected_char: str, type: TokenType, value: Any | None = None):
        if not (c := self.peek()):
            raise ValueError("Unexpected end of file")
        if c and c == expected_char:
            self.pos += 1
            return Token(c, type, value)
        raise ValueError(f"Expected character {expected_char} got {c}")

    def tokenize(self):
        while (c := self.peek()) is not None:
            match c:
                case "\n" | "\t" | " " | "":
                    self.pos += 1
                case "~":
                    self.tokens.append(self.consume("~", TokenType.NOT))
                case "^":
                    self.tokens.append(self.consume("^", TokenType.AND))
                case "v":
                    self.tokens.append(self.consume("v", TokenType.OR))
                case "(":
                    self.tokens.append(self.consume("(", TokenType.OPEN_P))
                case ")":
                    self.tokens.append(self.consume(")", TokenType.CLOSE_P))
                case "=":
                    self.tokens.append(self.consume("=", TokenType.EQUAL))
                case "0" | "1":
                    self.pos += 1
                    self.tokens.append(Token(c, TokenType.LITERAL, c))
                case ":" if self.peek(1) == "=":
                    self.consume(":", TokenType.COLON)
                    self.consume("=", TokenType.EQUAL)
                    self.tokens.append(Token(":=", TokenType.ASSIGN))
                case _ if c.isalpha():
                    self.pos += 1
                    identifier = c
                    while c := self.peek():
                        if c not in RESERVED_SYMBOLS:
                            self.pos += 1
                            identifier += c
                        else:
                            break
                    self.tokens.append(
                        Token(identifier, TokenType.IDENTIFIER, identifier)
                    )
                case _:
                    raise ValueError(f"Invalid Character: {c}")

        return self.tokens
