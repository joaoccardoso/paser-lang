from typing import Any
from logic_parser.exceptions import TokenizerError
from logic_parser.token import Token, TokenType

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
    TokenType.COMMA.value,
]


class Tokenizer:
    def __init__(self, content: str) -> None:
        self.content = content
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.line_pos = 0

    def peek(self, next: int = 0):
        if self.pos + next < len(self.content):
            return self.content[self.pos + next]
        return None

    def consume(self, expected_char: str, type: TokenType, value: Any | None = None):
        if not (c := self.peek()):
            raise TokenizerError(
                "Unexpected end of file", line=self.line, line_pos=self.line_pos
            )
        if c and c == expected_char:
            self.pos += 1
            self.line_pos += 1
            return Token(
                token=c,
                type=type,
                line=self.line,
                line_pos=self.line_pos,
                value=value,
            )
        raise TokenizerError(
            f"Expected character '{expected_char}' got '{c}'",
            line=self.line,
            line_pos=self.line_pos,
        )

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
                case ",":
                    self.tokens.append(self.consume(",", TokenType.COMMA))
                case "/" if self.peek(1) == "/":
                    self.consume("/", TokenType.SLASH)
                    self.consume("/", TokenType.SLASH)
                    comment = ""
                    while t := self.peek():
                        if t == "\n":
                            break
                        comment += t
                        self.pos += 1
                        self.line_pos += 1
                    self.tokens.append(
                        Token(
                            token="//",
                            type=TokenType.COMMENT,
                            line=self.line,
                            line_pos=self.line_pos,
                            value=comment,
                        )
                    )
                case "<" if self.peek(1) == "=" and self.peek(2) == ">":
                    self.consume("<", TokenType.LESS)
                    self.consume("=", TokenType.EQUAL)
                    self.consume(">", TokenType.GREATER)
                    self.tokens.append(
                        Token(
                            token="<=>",
                            type=TokenType.BICONDITIONAL,
                            line=self.line,
                            line_pos=self.line_pos,
                        )
                    )
                case "=" if self.peek(1) == ">":
                    self.consume("=", TokenType.EQUAL)
                    self.consume(">", TokenType.GREATER)
                    self.tokens.append(
                        Token(
                            token="=>",
                            type=TokenType.IMPLICATION,
                            line=self.line,
                            line_pos=self.line_pos,
                        )
                    )
                case "=":
                    self.tokens.append(self.consume("=", TokenType.EQUAL))
                case "!" if self.peek(1) == "=":
                    self.consume("!", TokenType.BANG)
                    self.consume("=", TokenType.EQUAL)
                    self.tokens.append(
                        Token(
                            token="!=",
                            type=TokenType.XOR,
                            line=self.line,
                            line_pos=self.line_pos,
                        )
                    )
                case "0" | "1":
                    self.pos += 1
                    self.line_pos += 1
                    self.tokens.append(
                        Token(
                            token=c,
                            type=TokenType.LITERAL,
                            line=self.line,
                            line_pos=self.line_pos,
                            value=c,
                        )
                    )
                case ":" if self.peek(1) == "=":
                    self.consume(":", TokenType.COLON)
                    self.consume("=", TokenType.EQUAL)
                    self.tokens.append(
                        Token(
                            token=":=",
                            type=TokenType.ASSIGN,
                            line=self.line,
                            line_pos=self.line_pos,
                        )
                    )
                case _ if c.isalpha():
                    self.pos += 1
                    self.line_pos += 1
                    identifier = c
                    while c := self.peek():
                        if c not in RESERVED_SYMBOLS:
                            self.pos += 1
                            self.line_pos += 1
                            identifier += c
                        else:
                            break
                    self.tokens.append(
                        Token(
                            token=identifier,
                            type=TokenType.IDENTIFIER,
                            line=self.line,
                            line_pos=self.line_pos,
                            value=identifier,
                        )
                    )
                case "\n":
                    self.line += 1
                    self.tokens.append(self.consume("\n", TokenType.NEW_LINE))
                    self.line_pos = 0
                case "\t" | " " | "":
                    self.pos += 1
                    self.line_pos += 1
                case _:
                    raise TokenizerError(
                        f"Invalid Character: '{c}'",
                        line=self.line,
                        line_pos=self.line_pos,
                    )

        return self.tokens
