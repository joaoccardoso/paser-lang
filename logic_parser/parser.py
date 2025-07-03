import abc
from dataclasses import dataclass
from typing import Any
from logic_parser.token import Token, TokenType


class Expr(abc.ABC):
    @abc.abstractmethod
    def eval(self): ...


@dataclass
class ValueExpr(Expr):
    value: Any

    def eval(self):
        return self.value


@dataclass
class UnaryExpr(Expr):
    operator: TokenType
    operand: Expr

    def eval(self):
        match self.operator:
            case TokenType.NOT:
                return not self.operand.eval()
            case _:
                raise NotImplementedError(f"Operator {self.operator} not implemented.")


@dataclass
class BinaryExpr(Expr):
    operator: TokenType
    r_operand: Expr
    l_operand: Expr

    def eval(self):
        match self.operator:
            case TokenType.OR:
                return self.r_operand.eval() or self.l_operand.eval()
            case TokenType.AND:
                return self.r_operand.eval() and self.l_operand.eval()
            case _:
                raise NotImplementedError(f"Operator {self.operator} not implemented.")


class NoneExpr(Expr):
    def eval(self):
        return None


class Parser:
    def __init__(self, tokens: list[Token], memory: dict[str, Any] = {}) -> None:
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

    def parse(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while (t := self.peek()) and t.type == TokenType.OR:
            self.consume(TokenType.OR)
            right = self.parse_and()
            node = BinaryExpr(TokenType.OR, node, right)
        return node

    def parse_and(self):
        node = self.parse_not()
        while (t := self.peek()) and t.type == TokenType.AND:
            self.consume(TokenType.AND)
            right = self.parse_not()
            node = BinaryExpr(TokenType.AND, node, right)
        return node

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
            else:
                value = self.memory.get(key)
                if value is None:
                    raise SyntaxError(f"No value found for variable name {key}")
                if isinstance(value, Expr):
                    return value
                return ValueExpr(value)
        elif t and t.type == TokenType.OPEN_P:
            self.consume(TokenType.OPEN_P)
            expr = self.parse_or()
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
            match value:
                case "0":
                    return False
                case "1":
                    return True
                case _:
                    raise NotImplementedError(f"Unknown literal: {value}")
        else:
            return self.parse()
