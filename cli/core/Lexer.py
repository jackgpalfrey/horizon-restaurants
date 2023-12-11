from dataclasses import dataclass
from src.utils.enum import Enum, iota


class TokenKind(Enum):
    EOF = iota(True)


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

        tokens.append(self.token(TokenKind.EOF, len(
            self.source), len(self.source), ''))
        return tokens

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
