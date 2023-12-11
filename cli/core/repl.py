from pprint import pprint
from Lexer import Lexer

lexer = Lexer("")
tokens = lexer.create_tokens()
pprint(tokens)
