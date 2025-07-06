import sys
from logic_parser.exceptions import ParserError, TokenizerError
from logic_parser.repl import REPL
from logic_parser.parser import Parser
from logic_parser.tokenizer import Tokenizer


def usage():
    print("Usage:")
    print("  python -m logic_parser.main [file]")
    print("    [file]   Path to a file with logic expressions to evaluate.")
    print("    -h      Show this help message.")
    print("If no file is provided, starts the interactive REPL.")


def run_file(file_path: str):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        tokens = Tokenizer(content).tokenize()
        for result in Parser(tokens).parse_all():
            print(result.eval())
    except TokenizerError as t_err:
        print(f"{file_path}:{t_err.line}:{t_err.line_pos + 1}: {t_err}.")
        exit(1)
    except ParserError as p_err:
        if p_err.token:
            print(
                f"{file_path}:{p_err.token.line}:{p_err.token.line_pos + 1}: {p_err}."
            )
        else:
            print(f"{file_path}: {p_err}.")
        exit(1)
    except Exception as e:
        print(f"{file_path}: {e}.")
        exit(1)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h":
            usage()
            return

        run_file(sys.argv[1])

    else:
        REPL().run()


if __name__ == "__main__":
    main()
