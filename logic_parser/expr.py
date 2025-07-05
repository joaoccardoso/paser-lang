import abc
from dataclasses import dataclass
from typing import Any

from logic_parser.token import TokenType


class Expr(abc.ABC):
    @abc.abstractmethod
    def eval(self) -> bool: ...


@dataclass
class LiteralExpr(Expr):
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
        A = self.r_operand.eval()
        B = self.l_operand.eval()
        match self.operator:
            case TokenType.BICONDITIONAL:
                return (A and B) or (not A and not B)
            case TokenType.IMPLICATION:
                return (not A) or B
            case TokenType.OR:
                return A or B
            case TokenType.XOR:
                return (A or B) and not (A and B)
            case TokenType.AND:
                return A and B
            case _:
                raise NotImplementedError(f"Operator {self.operator} not implemented.")


class NoneExpr(Expr):
    def eval(self):
        return None
