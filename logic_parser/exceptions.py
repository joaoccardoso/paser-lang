from logic_parser.token import Token


class TokenizerError(Exception):
    def __init__(self, *args: object, line: int, line_pos: int) -> None:
        self.line = line
        self.line_pos = line_pos
        super().__init__(*args)


class ParserError(Exception):
    def __init__(self, *args: object, token: Token | None = None) -> None:
        self.token = token
        super().__init__(*args)
