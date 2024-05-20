# https://craftinginterpreters.com/
# https://github.com/TodePond/DreamBerd

"""
TODO:
    [] - I want statement termination to be handled syntactically the way Python does it. (I think. This comes at the cost of in-line functions MUST be 1 line)
    [] - I want the pipe operator |> to be native to the language. I think I want this to handle return values being passed from one function as arguments to another.
    [] - I want to include variable state. namely the concept of a `taint`ed variable (Perl)
"""

from .token import TokenType, Token
from .scanner import Scanner
from .expressions import BinaryExpr


class Lox:
    def __init__(self):
        self.has_error = False
        # self.scanner = Scanner()

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.has_error = True

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def run(self, source: str):
        tokens = self.scanner.scan_tokens(source)
        for token in tokens:
            print(token)

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            self.run(line)

    def run_file(self, path: str):
        with open(path, "rb") as f:
            self.run(f.read())

    def Main(self, args: list[str]):
        if len(args) > 1:
            print("Usage: lox.py [script]")
            raise SystemExit(64)
        elif len(args) == 1:
            self.run_file(args[0])
        else:
            self.run_prompt()
