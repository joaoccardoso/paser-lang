from dataclasses import dataclass
from typing import Callable
from logic_parser.exceptions import ParserError
from logic_parser.expr import BinaryExpr, Expr, LiteralExpr, NoneExpr, UnaryExpr
from logic_parser.token import Token, TokenType


@dataclass
class Function:
    name: str
    args: list[str]
    tokens: list[Token]


class Parser:
    def __init__(
        self, tokens: list[Token], memory: dict[str, Expr | bool] = {}
    ) -> None:
        self.tokens = tokens
        self.memory = memory
        self.functions: dict[str, Function] = {}
        self.pos = 0

    def peek(self, next: int = 0):
        pos = self.pos + next
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def consume(self, expected_type: TokenType):
        if not (t := self.peek()):
            raise ParserError("Unexpected end of input", token=t)
        if t.type != expected_type:
            raise ParserError(
                f"Expected type '{expected_type.value}' got '{t.type.value}'",
                token=t,
            )
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
                raise ParserError(f"Invalid variable name '{key}'", token=t)

            next_t = self.peek()

            if next_t and next_t.type == TokenType.OPEN_P:
                self.consume(TokenType.OPEN_P)
                args = []
                while next_t := self.peek():
                    arg_id = self.consume(TokenType.IDENTIFIER)
                    args.append(arg_id.token)
                    next_t = self.peek()
                    if not next_t:
                        raise ParserError("Invalid function declaration", token=next_t)
                    if next_t.type == TokenType.CLOSE_P:
                        self.consume(TokenType.CLOSE_P)
                        break
                    elif next_t.type == TokenType.COMMA:
                        self.consume(TokenType.COMMA)
                    else:
                        raise ParserError("Invalid function declaration", token=next_t)

                next_t = self.peek()
                if next_t and next_t.type == TokenType.ASSIGN:
                    self.consume(TokenType.ASSIGN)
                    func_tokens = []
                    while func_t := self.peek():
                        self.consume(func_t.type)
                        if func_t.type == TokenType.NEW_LINE:
                            break
                        func_tokens.append(func_t)

                    self.functions[key] = Function(key, args, func_tokens)
                    return self.parse()

                if next_t and next_t.type == TokenType.COMMA:
                    func = self.functions[key]
                    if len(args) != len(func.args):
                        raise ParserError(
                            f"Expected {len(func.args)} arguments for function '{func.name}', got {len(args)}",
                            token=next_t,
                        )

                    local_memory = {}
                    for i, arg in enumerate(func.args):
                        if val := self.memory.get(args[i]):
                            local_memory[arg] = val
                        else:
                            raise ParserError(
                                f"No value found for variable name '{key}'", token=t
                            )

                    local_parser = Parser(func.tokens, local_memory)
                    return local_parser.parse()

            if next_t and next_t.type == TokenType.ASSIGN:
                self.consume(TokenType.ASSIGN)
                value = self.parse_assignment()
                self.memory[key] = value
                return self.parse()

            value = self.memory.get(key)
            if value is None:
                raise ParserError(f"No value found for variable name '{key}'", token=t)
            if isinstance(value, Expr):
                return value
            if isinstance(value, Token):
                if value.value == "0":
                    return LiteralExpr(False)
                if value.value == "1":
                    return LiteralExpr(True)
                else:
                    raise ParserError(
                        f"Invalid token value '{value.value}'",
                        token=next_t,
                    )
            if isinstance(value, bool):
                return LiteralExpr(value)
            else:
                raise ParserError(f"Invalid assignment value '{value}'", token=next_t)
        elif t and t.type == TokenType.OPEN_P:
            self.consume(TokenType.OPEN_P)
            expr = self.parse()
            self.consume(TokenType.CLOSE_P)
            return expr
        else:
            raise ParserError(f"Unexpected Token: '{t.token}'", token=t)

    def parse_assignment(self):
        t = self.peek()
        if not t:
            raise ParserError(
                "Invalid assignment syntax. Variables should receive Identifiers, Literals or Expressions",
                token=t,
            )

        if t.type == TokenType.LITERAL:
            value = self.consume(TokenType.LITERAL).value
            if next_t := self.peek():
                if next_t.type not in [TokenType.NEW_LINE]:
                    raise ParserError(
                        "Invalid variable assignment. It should be followed by new line or a ','",
                        token=t,
                    )
                self.consume(next_t.type)
            match value:
                case "0":
                    return LiteralExpr(False)
                case "1":
                    return LiteralExpr(True)
                case _:
                    raise NotImplementedError(f"Unknown literal: {value}")

        next_t = self.peek(1)
        if (
            t.type == TokenType.IDENTIFIER
            and isinstance(t.value, str)
            and next_t
            and next_t.type == TokenType.OPEN_P
        ):
            self.consume(TokenType.IDENTIFIER)
            self.consume(TokenType.OPEN_P)

            if not (func := self.functions.get(t.value)):
                raise ParserError(f"Function named '{t.value}' not found")

            expected_args = args = func.args
            args = []
            while next_t := self.peek():
                arg = self.parse()
                args.append(arg)
                next_t = self.peek()
                if not next_t:
                    raise ParserError("Invalid function usage", token=next_t)
                if next_t.type == TokenType.CLOSE_P:
                    self.consume(TokenType.CLOSE_P)
                    break
                elif next_t.type == TokenType.COMMA:
                    self.consume(TokenType.COMMA)
                else:
                    raise ParserError("Invalid function usage", token=next_t)

            if len(args) != len(expected_args):
                raise ParserError(
                    f"Expected {len(expected_args)} arguments for function '{func.name}', got {len(args)}",
                    token=next_t,
                )

            local_memory = {arg: args[i] for i, arg in enumerate(expected_args)}
            local_parser = Parser(func.tokens, local_memory)

            return local_parser.parse()

        else:
            return self.parse()
