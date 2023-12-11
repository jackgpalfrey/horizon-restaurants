import importlib
import inspect
from types import ModuleType
from typing import Callable
from Parser import *
from errors import *
from cli.libs.stdlib import echo
from CLI import Env

LIBRARY_PATH = "cli.libs"


class Evaluator:
    def __init__(self) -> None:
        self._libraries: dict[str, ModuleType] = {}
        self._commands: dict[str, Callable] = {}
        self.ctx: dict[str, any] = {}

    def evaluate(self, source: str) -> any:
        parser = Parser()
        ast = parser.parse_from_source(source)

        return self._evaluate_ast(ast)

    def include(self, libname: str) -> None:
        """"
        Adds library under cli/libs/<lib> to the evaluator's scope.
        """

        lib_path = f"{LIBRARY_PATH}.{libname}"
        lib = importlib.import_module(lib_path)

        self._include_module(libname, lib)

    def reload(self) -> None:
        """
        Reloads all libraries that have been included into the evaluator.
        """

        self._commands.clear()

        libs = list(self._libraries.items())

        for lib, module in libs:
            new_module = importlib.reload(module)
            self._include_module(lib, new_module)

    def _include_module(self, name: str, module: ModuleType) -> None:
        functions = inspect.getmembers(module, inspect.isfunction)

        for name, func in functions:
            self._add_command(name, func)

        self._libraries[name] = module

    def _evaluate_ast(self, ast: ProgramStmt) -> any:
        for line in ast.lines:
            return self._evaluate_line(line)

    def _evaluate_line(self, line: ProgramLineStmt):
        command = line.command
        args = line.args

        return self._execute(command, args)

    def _execute(self, command: str, args: list[Expression]) -> any:
        func = self._commands.get(command, None)
        if func is None:
            raise CommandError(f"Command '{command}' not found")

        try:
            return self._execute_command(func, args)
        except (ArgError, TypeError) as e:
            print(self._get_usage(func))

    def _get_usage(self, func: Callable) -> str:
        docs = inspect.getdoc(func)
        if docs is not None:
            return docs.splitlines()[0]

        spec = inspect.getfullargspec(func)
        args = spec.args
        vararg = spec.varargs
        kwargs = spec.kwonlyargs

        usage = f"Usage: {func.__name__} "

        for arg in args:
            usage += f"<{arg}> "

        if vararg is not None:
            usage += f"[<{vararg}> ...] "

        for kwarg in kwargs:
            usage += f"[--{kwarg} <{kwarg}>] "

        return usage

    def _execute_command(self, func: Callable, args_and_kwargs: list[Expression]) -> any:
        args, kwargs = self.split_args_and_kwargs(args_and_kwargs)
        spec = inspect.getfullargspec(func)

        fnc_args = spec.args
        fnc_vararg = spec.varargs
        fnc_types = spec.annotations
        fnc_kwargs = spec.kwonlyargs

        input_args = []

        arg_ptr = 0

        first_arg = fnc_args[0] if len(fnc_args) > 0 else None
        first_type = fnc_types.get(first_arg, None)

        try:
            if (first_type.IS_ENV == True):
                input_args.append(Env(self))
                fnc_args.pop(0)
        except:
            pass

        match first_type:
            case Env():
                print("INSERT")
                input_args.append(Env(self))
                fnc_args.pop(0)

        while arg_ptr < len(fnc_args) and arg_ptr < len(args):
            arg = self._evaluate_expression(args[arg_ptr])
            expected_arg = fnc_args[arg_ptr]
            expected_arg_type = fnc_types.get(expected_arg, None)

            self._check_type_and_raise(arg_ptr, arg, expected_arg_type)
            input_args.append(arg)
            arg_ptr += 1

        if arg_ptr < len(args):
            if fnc_vararg is None or fnc_vararg == "_":
                raise ArgError(
                    f"Expected {len(fnc_args)} arguments, got {len(args)}")

            for arg in args[arg_ptr:]:
                arg = self._evaluate_expression(arg)
                expected_type = fnc_types.get(fnc_vararg, None)
                self._check_type_and_raise(arg_ptr, arg, expected_type)
                input_args.append(arg)

        inp_kwargs = {}
        for ex_kwarg in fnc_kwargs:
            kwarg_val = None

            if ex_kwarg in kwargs:
                kwarg_val = self._evaluate_expression(kwargs[ex_kwarg])

                expected_kwarg_type = fnc_types.get(ex_kwarg, None)
                self._check_type_and_raise(
                    ex_kwarg, kwarg_val, expected_kwarg_type)

                inp_kwargs[ex_kwarg] = kwarg_val
            else:
                inp_kwargs[ex_kwarg] = None

        return func(*input_args, **inp_kwargs)

    def split_args_and_kwargs(self, args_and_kwargs: list[Expression]) -> tuple[list[Expression], dict[str, Expression]]:
        """
        :returns: (args, kwargs)
        """

        args = []
        kwargs = {}

        for arg in args_and_kwargs:
            if isinstance(arg, FlagExpr):
                kwargs[arg.name] = arg.value
            else:
                args.append(arg)

        return (args, kwargs)

    def _evaluate_expression(self, expr: Expression) -> any:
        match expr:
            case SymbolLitExpr():
                return expr.value
            case IntegerLitExpr():
                return expr.value
            case FloatLitExpr():
                return expr.value
            case BooleanLitExpr():
                return expr.value
            case StringLitExpr():
                return expr.value

    def _check_type_and_raise(self, arg_idx: int, value: any, expected_type: any) -> bool:
        ex_arg_exists = expected_type is not None
        arg_type_matches = isinstance(value, expected_type)
        if ex_arg_exists and not arg_type_matches:
            raise ArgError(
                f"Expected argument {arg_idx} to be of type {expected_type}, got {type(value)}")

        return True

    def _add_command(self, name: str, func: Callable) -> None:
        self._commands[name] = func
