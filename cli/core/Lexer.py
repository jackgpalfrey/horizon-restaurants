import re

from dataclasses import dataclass
from src.utils.enum import Enum, iota

DIGIT_REGEX = re.compile(r'[0-9]')
SYMBOL_REGEX = re.compile(r'[a-zA-Z0-9_]')


def is_digit(char: str) -> bool:
    return DIGIT_REGEX.match(char)


def is_symbol(char: str) -> bool:
    return SYMBOL_REGEX.match(char)


class TokenKind(Enum):
    Integer = iota(True)
    Float = iota()
    Symbol = iota()

    EOF = iota()


@dataclass()
class Token:
    kind: TokenKind
    start: int
    end: int
    text: str


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.ptr = -1

    def create_tokens(self) -> list[Token]:
        tokens = []

        while self.not_eof():
            token = self.lex_next()
            if token is not None:
                tokens.append(token)

        tokens.append(self.token(TokenKind.EOF, len(
            self.source), len(self.source), ''))
        return tokens

    def lex_next(self) -> Token:
        char = self.advance()

        match char:
            case " " | "\n":
                return

        if is_digit(char):
            return self.lex_number()

        if is_symbol(char):
            return self.lex_symbol()

        raise Exception(f"Unexpected character: {char}")

    def lex_number(self) -> Token:
        start = self.ptr

        while self.not_eof() and is_digit(self.peek()):
            self.advance()

        if self.peek() == '.':
            self.advance()  # Eat the '.'
            while self.not_eof() and is_digit(self.peek()):
                self.advance()

            return self.token(TokenKind.Float, start)

        return self.token(TokenKind.Integer, start)

    def lex_symbol(self) -> Token:
        start = self.ptr

        while self.not_eof() and is_symbol(self.peek()):
            self.advance()

        return self.token(TokenKind.Symbol, start)

    def token(self, kind: TokenKind, start: int = None, end: int = None, text: str = None) -> Token:
        """
        Returns a token with the given kind, start, end, and text.

        :param kind: The kind of token.
        :param start: The start index of the token (inclusive)
        :param end: The end index of the token (exclusive)
        :param text: The text of the token.

        """
        if start is None:
            start = self.ptr

        if end is None:
            end = self.ptr + 1

        if text is None:
            text = self.source[start:end]

        return Token(kind, start, end - 1, text)

    def advance(self) -> str:
        """
        Returns the current character and advances the pointer to the next character.
        """
        self.ptr += 1
        return self.source[self.ptr]

    def peek(self) -> str:
        """
        Returns the next character without advancing the pointer.
        """
        try:
            return self.source[self.ptr + 1]
        except IndexError:
            return ''

    def not_eof(self):
        return self.ptr + 1 < len(self.source)
