from pprint import pprint
from Lexer import Lexer
from Parser import Parser
from Evaluator import Evaluator
from errors import CLIError


try:
    while True:
        inp = input("horizon-cli > ")

        if inp == "exit":
            break

        try:
            evaluator = Evaluator()
            result = evaluator.evaluate(inp)
            print(result)
        except CLIError as e:
            print(f"{e.__class__}: {e.message}")


except KeyboardInterrupt:
    print("Exiting softly...")
