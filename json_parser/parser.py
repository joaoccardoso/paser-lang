from json_parser.token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type: TokenType | None = None):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected type {expected_type} got {token.type}")

        self.pos += 1
        return token

    def parse(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        match token.type:
            case TokenType.OPEN_CURLY_BRACKETS:
                return self.parse_object()
            case TokenType.OPEN_BRACKETS:
                return self.parse_list()
            case TokenType.STRING:
                return self.consume(TokenType.STRING).value
            case TokenType.NUMBER:
                value = self.consume(TokenType.NUMBER).value
                if value is None:
                    raise SyntaxError("Expected token value to be number got null")
                elif isinstance(value, float) or isinstance(value, int):
                    return value
                elif isinstance(value, str):
                    if len(value) == 0:
                        raise SyntaxError(
                            "Expected token value to be number got empty string"
                        )
                    if "." in value:
                        return float(value)
                    else:
                        return int(value)
                else:
                    raise SyntaxError(
                        f"Expected token value to be number got {type(value)}"
                    )
            case TokenType.TRUE:
                self.consume(TokenType.TRUE)
                return True
            case TokenType.FALSE:
                self.consume(TokenType.FALSE)
                return False
            case TokenType.NULL:
                self.consume(TokenType.NULL)
                return None
            case _:
                raise SyntaxError(f"Unexpected Token {token}")

    def parse_object(self):
        obj = {}
        self.consume(TokenType.OPEN_CURLY_BRACKETS)
        next_token = self.peek()
        while (
            next_token is not None and next_token.type != TokenType.CLOSE_CURLY_BRACKETS
        ):
            key = self.consume(TokenType.STRING).value
            self.consume(TokenType.COLON)
            value = self.parse()
            obj[key] = value
            next_token = self.peek()
            if next_token and next_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        self.consume(TokenType.CLOSE_CURLY_BRACKETS)
        return obj

    def parse_list(self):
        arr = []
        self.consume(TokenType.OPEN_BRACKETS)
        next_token = self.peek()
        while next_token is not None and next_token.type != TokenType.CLOSE_BRACKETS:
            arr.append(self.parse())
            next_token = self.peek()
            if next_token and next_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        self.consume(TokenType.CLOSE_BRACKETS)
        return arr
