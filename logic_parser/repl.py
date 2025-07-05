from logic_parser.parser import Parser
from logic_parser.token import Tokenizer


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
        except Exception as e:
            print(e)

        return True
