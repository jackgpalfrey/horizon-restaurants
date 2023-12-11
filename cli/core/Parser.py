from __future__ import annotations
from Lexer import *
from errors import ParseError


class Statement:
    pass


@dataclass
class ProgramStmt(Statement):
    lines: list[ProgramLineStmt]


@dataclass
class ProgramLineStmt(Statement):
    command: str
    args: list[Expression]
    pass


class Expression:
    pass


@dataclass
class FlagExpr(Expression):
    name: str
    value: LiteralExpr


class LiteralExpr(Expression):
    pass


@dataclass
class SymbolLitExpr(LiteralExpr):
    value: str


@dataclass
class IntegerLitExpr(LiteralExpr):
    value: int


@dataclass
class FloatLitExpr(LiteralExpr):
    value: float


@dataclass
class BooleanLitExpr(LiteralExpr):
    value: bool


class Parser:
    def __init__(self) -> None:
        self.tokens: list[Token] = []
        self.ptr = -1

    def parse_from_source(self, source: str) -> ProgramStmt:
        lexer = Lexer(source)
        self.tokens = lexer.create_tokens()

        return self._create_ast()

    def _create_ast(self) -> ProgramStmt:
        lines: list[ProgramLineStmt] = []

        while self.not_eof():
            lines.append(self._parse_line())

        return ProgramStmt(lines)

    def _parse_line(self) -> ProgramLineStmt:
        if not self.not_eof():
            return ProgramLineStmt("", [])

        command = self.advance_expect(TokenKind.Symbol).text
        args: list[Expression] = []

        while self.not_eof():
            expr = self._parse_expression()
            if isinstance(expr, list):
                args.extend(expr)
            else:
                args.append(expr)

        return ProgramLineStmt(command, args)

    def _parse_expression(self) -> Expression | list[Expression]:
        return self._parse_flag()

    def _parse_flag(self) -> Expression | list[Expression]:
        match self.peek().kind:
            case TokenKind.MINUS:
                return self._parse_char_flag()
            case TokenKind.DMINUS:
                return self._parse_double_flag()
            case _:
                return self._parse_primary_expression()

    def _parse_char_flag(self) -> Expression | list[Expression]:
        self.advance()  # EAT MINUS
        symbol_text = self.advance_expect(TokenKind.Symbol).text
        flags = []
        for char in symbol_text:
            flags.append(FlagExpr(char, BooleanLitExpr(True)))

        return flags

    def _parse_double_flag(self) -> Expression:
        self.advance()  # Eat DMINUS
        flag_name = self.advance_expect(TokenKind.Symbol).text
        if self.peek().kind == TokenKind.EQUALS:
            self.advance()  # EAT EQUALS
            flag_value = self._parse_expression()
        else:
            flag_value = BooleanLitExpr(True)

        return FlagExpr(flag_name, flag_value)

    def _parse_primary_expression(self) -> Expression:
        match self.peek().kind:
            case TokenKind.Symbol:
                return SymbolLitExpr(self.advance().text)
            case TokenKind.Integer:
                return IntegerLitExpr(int(self.advance().text))
            case TokenKind.Float:
                return FloatLitExpr(float(self.advance().text))
            case _:
                raise ParseError(
                    f"Unexpected token {self.peek().kind} at {self.peek().start}")

    def advance(self) -> Token:
        self.ptr += 1
        return self.tokens[self.ptr]

    def advance_expect(self, kind: TokenKind):
        token = self.advance()
        if token.kind != kind:
            raise ParseError(f"Expected {kind} but got {token.kind}")

        return token

    def peek(self) -> Token:
        return self.tokens[self.ptr + 1]

    def not_eof(self) -> bool:
        return self.peek().kind != TokenKind.EOF
