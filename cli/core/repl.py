import time
from pprint import pprint
from Evaluator import Evaluator
from errors import CLIError

START_DELAY = 500
START_DOT_INTERVAL = 100


evaluator = Evaluator()
evaluator.include("stdlib")
evaluator.include("init")
evaluator.init()


for i in range(START_DELAY // START_DOT_INTERVAL):
    print("\rStarting CLI" + "." * i, end="")
    time.sleep(START_DOT_INTERVAL / 1000)


print("\nCLI started. Type 'help' for help.")


try:
    while True:
        try:
            prompt_str = evaluator.evaluate("prompt")
        except CLIError:
            prompt_str = "> "
        inp = input(prompt_str)

        try:
            result = evaluator.evaluate(inp)
            print("-> ", end="")
            pprint(result)
        except CLIError as e:
            print(f"{e.__class__.__name__}: {e.message}")


except KeyboardInterrupt:
    print("Exiting softly...")
