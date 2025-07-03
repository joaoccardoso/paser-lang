from logic_parser import token
from logic_parser.parser import Parser


def main():
    stmt = """
        A = 1
        B = 0
        C = 1
        R = ~(A^B)vC
        R
    """

    tokens = token.tokenize(stmt)

    parser = Parser(tokens)
    result = parser.parse()

    print(f"Result: {result.eval()}")


if __name__ == "__main__":
    main()
