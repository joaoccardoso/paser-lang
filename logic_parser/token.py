from dataclasses import dataclass
import enum
from typing import Any, Optional


class TokenType(enum.Enum):
    WHITESPACE = ""
    NEW_LINE = "\n"

    OPEN_P = "("
    CLOSE_P = ")"

    COMMENT = "//"

    # Value Tokens
    IDENTIFIER = "IDENTIFIER"
    LITERAL = "LITERAL"

    # Operators
    OR = "v"
    AND = "^"
    NOT = "~"
    IMPLICATION = "=>"
    BICONDITIONAL = "<=>"
    XOR = "!="

    GREATER = ">"
    LESS = "<"
    BANG = "!"
    EQUAL = "="
    COLON = ":"
    ASSIGN = ":="
    SLASH = "/"


RESERVED_SYMBOLS = [
    " ",
    TokenType.WHITESPACE.value,
    TokenType.NEW_LINE.value,
    TokenType.OPEN_P.value,
    TokenType.CLOSE_P.value,
    TokenType.AND.value,
    TokenType.NOT.value,
    TokenType.GREATER.value,
    TokenType.LESS.value,
    TokenType.BANG.value,
    TokenType.EQUAL.value,
    TokenType.COLON.value,
    TokenType.SLASH.value,
]


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
                case "/" if self.peek(1) == "/":
                    self.consume("/", TokenType.SLASH)
                    self.consume("/", TokenType.SLASH)
                    comment = ""
                    while t := self.peek():
                        if t == "\n":
                            break
                        comment += t
                        self.pos += 1
                    self.tokens.append(Token("//", TokenType.COMMENT, comment))
                case "<" if self.peek(1) == "=" and self.peek(2) == ">":
                    self.consume("<", TokenType.LESS)
                    self.consume("=", TokenType.EQUAL)
                    self.consume(">", TokenType.GREATER)
                    self.tokens.append(Token("<=>", TokenType.BICONDITIONAL))
                case "=" if self.peek(1) == ">":
                    self.consume("=", TokenType.EQUAL)
                    self.consume(">", TokenType.GREATER)
                    self.tokens.append(Token("=>", TokenType.IMPLICATION))
                case "=":
                    self.tokens.append(self.consume("=", TokenType.EQUAL))
                case "!" if self.peek(1) == "=":
                    self.consume("!", TokenType.BANG)
                    self.consume("=", TokenType.EQUAL)
                    self.tokens.append(Token("!=", TokenType.XOR))
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
                case "\n":
                    self.tokens.append(self.consume("\n", TokenType.NEW_LINE))
                case "\t" | " " | "":
                    self.pos += 1
                case _:
                    raise ValueError(f"Invalid Character: {c}")

        return self.tokens
