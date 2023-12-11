from pprint import pprint
from Lexer import Lexer
from Parser import Parser
from Evaluator import Evaluator
from errors import CLIError

evaluator = Evaluator()
evaluator.include("stdlib")


try:
    while True:
        inp = input("horizon-cli > ")

        try:
            result = evaluator.evaluate(inp)
            print("-> ", end="")
            pprint(result)
        except CLIError as e:
            print(f"{e.__class__}: {e.message}")


except KeyboardInterrupt:
    print("Exiting softly...")
