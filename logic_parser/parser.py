from typing import Callable
from logic_parser.expr import BinaryExpr, Expr, LiteralExpr, NoneExpr, UnaryExpr
from logic_parser.token import Token, TokenType


class Parser:
    def __init__(
        self, tokens: list[Token], memory: dict[str, Expr | bool] = {}
    ) -> None:
        self.tokens = tokens
        self.memory = memory
        self.pos = 0

    def peek(self, next: int = 0):
        pos = self.pos + next
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def consume(self, expected_type: TokenType):
        if not (t := self.peek()):
            raise SyntaxError("Unexpected end of input")
        if t.type != expected_type:
            raise SyntaxError(f"Expected type {expected_type} got {t.type}")
        self.pos += 1
        return t

    def parse_binary_op(self, next_parse: Callable[[], Expr], type: TokenType):
        node = next_parse()
        while (t := self.peek()) and t.type == type:
            self.consume(type)
            right = next_parse()
            node = BinaryExpr(type, node, right)
        return node

    def parse_all(self):
        while self.pos < len(self.tokens):
            while (t := self.peek()) and t.type in [
                TokenType.WHITESPACE,
                TokenType.NEW_LINE,
            ]:
                self.consume(t.type)
            if self.pos >= len(self.tokens):
                break
            yield self.parse_commentary()

    def parse(self):
        return self.parse_commentary()

    def parse_commentary(self):
        if (t := self.peek()) and t.type == TokenType.COMMENT:
            self.consume(TokenType.COMMENT)
        return self.parse_biconditional()

    def parse_biconditional(self):
        return self.parse_binary_op(self.parse_implication, TokenType.BICONDITIONAL)

    def parse_implication(self):
        return self.parse_binary_op(self.parse_or, TokenType.IMPLICATION)

    def parse_or(self):
        return self.parse_binary_op(self.parse_xor, TokenType.OR)

    def parse_xor(self):
        return self.parse_binary_op(self.parse_and, TokenType.XOR)

    def parse_and(self):
        return self.parse_binary_op(self.parse_not, TokenType.AND)

    def parse_not(self):
        if (t := self.peek()) and t.type == TokenType.NOT:
            self.consume(TokenType.NOT)
            operand = self.parse_not()
            return UnaryExpr(TokenType.NOT, operand)
        else:
            return self.parse_identifier()

    def parse_identifier(self):
        if not (t := self.peek()):
            return NoneExpr()

        if t.type in [TokenType.NEW_LINE, TokenType.WHITESPACE]:
            self.consume(t.type)
            return self.parse()

        if t.type == TokenType.LITERAL:
            self.consume(TokenType.LITERAL)
            return LiteralExpr(t.value)

        if t and t.type == TokenType.IDENTIFIER:
            key = self.consume(TokenType.IDENTIFIER).value
            if not isinstance(key, str):
                raise SyntaxError(f"Invalid variable name {key}")

            next_t = self.peek()
            if next_t and next_t.type == TokenType.ASSIGN:
                self.consume(TokenType.ASSIGN)
                value = self.parse_assignment()
                self.memory[key] = value
                return self.parse()

            value = self.memory.get(key)
            if value is None:
                raise SyntaxError(f"No value found for variable name {key}")
            if isinstance(value, Expr):
                return value
            return LiteralExpr(value)
        elif t and t.type == TokenType.OPEN_P:
            self.consume(TokenType.OPEN_P)
            expr = self.parse()
            self.consume(TokenType.CLOSE_P)
            return expr
        else:
            raise SyntaxError(f"Unexpected Token: {t}")

    def parse_assignment(self):
        t = self.peek()
        if not t:
            raise SyntaxError(
                "Invalid assignment syntax. Variables should receive Identifiers, Literals or Expressions"
            )

        if t.type == TokenType.LITERAL:
            value = self.consume(TokenType.LITERAL).value
            if next_t := self.peek():
                if next_t.type not in [TokenType.NEW_LINE]:
                    raise SyntaxError(
                        "Invalid variable assignment. It should be followed by new line or a ','"
                    )
                self.consume(next_t.type)
            match value:
                case "0":
                    return LiteralExpr(False)
                case "1":
                    return LiteralExpr(True)
                case _:
                    raise NotImplementedError(f"Unknown literal: {value}")
        else:
            return self.parse()
