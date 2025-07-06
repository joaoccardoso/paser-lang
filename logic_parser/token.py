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


@dataclass
class Token:
    token: str
    type: TokenType
    line: int
    line_pos: int
    value: Optional[Any] = None
