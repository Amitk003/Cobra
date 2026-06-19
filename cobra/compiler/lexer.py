import re
from dataclasses import dataclass


TOKEN_SPEC = [
    ("NUMBER",    r"\d+(\.\d+)?"),
    ("STRING",    r'"[^"]*"'),
    ("STRING_SINGLE", r"'[^']*'"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("RANGE",     r"\.\."),
    ("ARROW",     r"->"),
    ("AND",       r"&&"),
    ("OR",        r"\|\|"),
    ("EQEQ",      r"=="),
    ("NEQ",       r"!="),
    ("LE",        r"<="),
    ("GE",        r">="),
    ("PLUS",      r"\+"),
    ("MINUS",     r"-"),
    ("STAR",      r"\*"),
    ("SLASH",     r"/"),
    ("LPAREN",    r"\("),
    ("RPAREN",    r"\)"),
    ("LBRACE",    r"\{"),
    ("RBRACE",    r"\}"),
    ("LBRACKET",  r"\["),
    ("RBRACKET",  r"\]"),
    ("EQ",        r"="),
    ("LT",        r"<"),
    ("GT",        r">"),
    ("NOT",       r"!"),
    ("DOT",       r"\."),
    ("COLON",     r":"),
    ("COMMA",     r","),
    ("NEWLINE",   r"\n"),
    ("SKIP",      r"[ \t]+"),
    ("COMMENT",   r"#.*"),
    ("MISMATCH",  r"."),
]

KEYWORDS = {
    "let": "LET",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "in": "IN",
    "func": "FUNC",
    "return": "RETURN",
    "import": "IMPORT",
    "true": "TRUE",
    "false": "FALSE",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
}


@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, L{self.line}:{self.col})"


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.line = 1
        self.col = 1

    def tokenize(self) -> list[Token]:
        pos = 0
        line = 1
        col = 1

        token_re = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
        for mo in re.finditer(token_re, self.source):
            kind = mo.lastgroup
            value = mo.group()
            start = mo.start()

            if kind == "SKIP":
                col += len(value)
                continue
            if kind == "COMMENT":
                continue
            if kind == "NEWLINE":
                line += 1
                col = 1
                self.tokens.append(Token("NEWLINE", "\n", line - 1, col))
                continue
            if kind == "MISMATCH":
                raise LexerError(f"Unexpected character {value!r} at line {line}, col {col}")

            if kind == "STRING_SINGLE":
                kind = "STRING"

            if kind == "IDENTIFIER" and value in KEYWORDS:
                kind = KEYWORDS[value]

            self.tokens.append(Token(kind, value, line, col))
            col += len(value)

        self.tokens.append(Token("EOF", "", line, col))
        return self.tokens
