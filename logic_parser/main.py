import sys
from logic_parser.repl import REPL
from logic_parser.token import Tokenizer
from logic_parser.parser import Parser


def usage():
    print("Usage:")
    print("  python -m logic_parser.main [file]")
    print("    [file]   Path to a file with logic expressions to evaluate.")
    print("    -h      Show this help message.")
    print("If no file is provided, starts the interactive REPL.")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h":
            usage()
            return
        with open(sys.argv[1], "r") as f:
            content = f.read()
        tokens = Tokenizer(content).tokenize()
        for result in Parser(tokens).parse_all():
            print(result.eval())

    else:
        REPL().run()


if __name__ == "__main__":
    main()
