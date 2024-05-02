from enum import Enum

# https://github.com/TodePond/DreamBerd

'''
TODO:
    [] - I want statement termination to be handled syntactically the way Python does it. (I think. This comes at the cost of in-line functions MUST be 1 line)
    [] - I want the pipe operator |> to be native to the language. I think I want this to handle return values being passed from one function as arguments to another.
'''

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    # One or two character tokens.
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19
    # Literals.
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22
    # Keywords.
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    MAYBE = 37
    VAR = 38
    WHILE = 39
    EOF = 40


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        hashmap = {
            "(": lambda: self.add_token(TokenType.LEFT_PAREN),
            ")": lambda: self.add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self.add_token(TokenType.LEFT_BRACE),
            "}": lambda: self.add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self.add_token(TokenType.COMMA),
            ".": lambda: self.add_token(TokenType.DOT),
            "-": lambda: self.add_token(TokenType.MINUS),
            "+": lambda: self.add_token(TokenType.PLUS),
            ";": lambda: self.add_token(TokenType.SEMICOLON),
            "*": lambda: self.add_token(TokenType.STAR),
            "!": lambda: self.add_token(
                TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            ),
            "=": lambda: self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            ),
            "<": lambda: self.add_token(
                TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            ),
            ">": lambda: self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            ),
            '"': lambda: self.add_string(),  # NOTE: only " for strings for now.
            # "'": lambda: self.add_string(),
        }
        try:
            hashmap[c]()
        except KeyError:
            pass
        if c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
                else:
                    self.add_token(TokenType.SLASH)
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
        else:
            Lox().error(self.line, f"Unexpected character: {c}")

    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_digit(self, char: str) -> bool:
        ordinal = ord(char)
        return ordinal >= ord("0") and ordinal <= ord("9")

    def is_alpha(self, char: str) -> bool:
        ordinal = ord(char)
        return (ordinal >= ord("a") and ordinal <= ord("z")) or (
            ordinal >= ord("A") and ordinal <= ord("Z")
        )

    def is_alphanumeric(self, char: str):
        return self.is_alpha(char) or self.is_digit(char)

    def add_digit(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def add_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            Lox().error(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def add_identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        text = self.source[self.start : self.current]
        keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "fun": TokenType.FUN,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }
        token_type = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"


class Lox:
    def __init__(self):
        self.has_error = False
        # self.scanner = Scanner(self)

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
