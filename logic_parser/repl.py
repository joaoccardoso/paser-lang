from logic_parser.exceptions import ParserError, TokenizerError
from logic_parser.parser import Parser
from logic_parser.tokenizer import Tokenizer


class REPL:
    def __init__(self) -> None:
        self.memory = {}

    def run(self):
        print("Positional Logic REPL")
        while self.eval_loop():
            ...

    def eval_loop(self):
        try:
            expr = input("?> ")
            if expr == "exit":
                print("\nExiting REPL")
                return False
            tokens = Tokenizer(expr).tokenize()
            parsed = Parser(tokens, self.memory).parse()
            result = parsed.eval()
            print(result)
        except KeyboardInterrupt:
            print("\nExiting REPL")
            return False
        except TokenizerError as t_err:
            print(f"Error at position {t_err.line_pos + 1}: {t_err}.")
        except ParserError as p_err:
            if p_err.token:
                print(f"Error at position {p_err.token.line_pos + 1}: {p_err}.")
            else:
                print(f"Error: {p_err}.")
        except Exception as e:
            print(e)

        return True
