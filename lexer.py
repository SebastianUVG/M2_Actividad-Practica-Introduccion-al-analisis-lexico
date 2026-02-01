# lexer.py

from token import Token
from symbol_table import SymbolTable


class Lexer:
    KEYWORDS = {
        "public", "class", "static", "final", "void",
        "int", "double", "String", "if", "else",
        "return", "new", "private", "this"
    }

    SYMBOLS = "{}();,+-*/=<>\n"

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.symbol_table = SymbolTable()

    def peek(self):
        if self.position < len(self.source):
            return self.source[self.position]
        return None

    def advance(self):
        char = self.peek()
        self.position += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def tokenize(self):
        while self.peek():
            char = self.peek()

            # Ignore whitespace
            if char.isspace():
                self.advance()
                continue

            # Line comment //
            if char == "/" and self._next_char() == "/":
                self._skip_line_comment()
                continue

            # Block comment /* */
            if char == "/" and self._next_char() == "*":
                self._skip_block_comment()
                continue

            # Identifiers / keywords
            if char.isalpha() or char == "_":
                self._tokenize_identifier()
                continue

            # Numbers
            if char.isdigit():
                self._tokenize_number()
                continue

            # Strings
            if char == '"':
                self._tokenize_string()
                continue

            # Symbols
            self.tokens.append(
                Token("SYMBOL", self.advance(), self.line, self.column)
            )

        return self.tokens
    
    def _skip_line_comment(self):
        # Consume "//"
        self.advance()
        self.advance()

        # Skip until end of line
        while self.peek() and self.peek() != "\n":
            self.advance()

    def _skip_block_comment(self):
        # Consume "/*"
        self.advance()
        self.advance()

        while self.peek():
            if self.peek() == "*" and self._next_char() == "/":
                self.advance()  # *
                self.advance()  # /
                break
            else:
                self.advance()


    def _next_char(self):
        if self.position + 1 < len(self.source):
            return self.source[self.position + 1]
        return None

    def _tokenize_identifier(self):
        start_col = self.column
        lexeme = ""

        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            lexeme += self.advance()

        if lexeme in self.KEYWORDS:
            token_type = "KEYWORD"
        else:
            token_type = "IDENTIFIER"
            self.symbol_table.add(lexeme, token_type)

        self.tokens.append(Token(token_type, lexeme, self.line, start_col))

    def _tokenize_number(self):
        start_col = self.column
        lexeme = ""
        dot_count = 0

        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                dot_count += 1
            lexeme += self.advance()

        self.tokens.append(Token("NUMBER", lexeme, self.line, start_col))

    def _tokenize_string(self):
        start_col = self.column
        lexeme = self.advance()  # opening quote

        while self.peek() and self.peek() != '"':
            lexeme += self.advance()

        if self.peek() == '"':
            lexeme += self.advance()

        self.tokens.append(Token("STRING", lexeme, self.line, start_col))

    def _skip_comment(self):
        while self.peek() and self.peek() != "\n":
            self.advance()
