import inspect
from typing import Callable
from Parser import *
from errors import *


class RuntimeValue:
    pass


def echonum(num: int | str) -> int:
    result = num
    print(result)
    return result


def echo(*text: str, p: bool = False, s: bool = False, repetitions: int = False) -> str:
    result = " ".join(text)

    if repetitions is not None:
        result = result * repetitions

    if p:
        result = "PREFIX: " + result

    print(result)
    return result


class Evaluator:
    def __init__(self) -> None:
        pass

    def evaluate(self, source: str) -> any:
        parser = Parser()
        ast = parser.parse_from_source(source)
        print(ast)

        self._add_command('echo', echonum)

        return self._evaluate_ast(ast)

    def _evaluate_ast(self, ast: ProgramStmt) -> any:
        for line in ast.lines:
            return self._evaluate_line(line)

    def _evaluate_line(self, line: ProgramLineStmt):
        command = line.command
        args = line.args

        return self._execute(command, args)

    def _execute(self, command: str, args: list[Expression]) -> any:
        match command:
            case 'echo':
                return self._execute_command(echo, args)

    def _execute_command(self, func: Callable, args_and_kwargs: list[Expression]) -> any:
        args, kwargs = self.split_args_and_kwargs(args_and_kwargs)

        print(args)

        spec = inspect.getfullargspec(func)

        fnc_args = spec.args
        fnc_vararg = spec.varargs
        fnc_types = spec.annotations
        fnc_kwargs = spec.kwonlyargs
        fnc_ret_type = fnc_types.get('return', None)

        # print(fnc_args)
        # print(fnc_vararg)
        # print(fnc_types)
        # print(fnc_defaults)
        print(fnc_kwargs)

        input_args = []

        arg_ptr = 0

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
            print(kwargs)

            if ex_kwarg in kwargs:
                kwarg_val = self._evaluate_expression(kwargs[ex_kwarg])

                expected_kwarg_type = fnc_types.get(ex_kwarg, None)
                self._check_type_and_raise(
                    ex_kwarg, kwarg_val, expected_kwarg_type)

                inp_kwargs[ex_kwarg] = kwarg_val
            else:
                inp_kwargs[ex_kwarg] = None

        print(inp_kwargs)
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

    def _check_type_and_raise(self, arg_idx: int, value: any, expected_type: any) -> bool:
        ex_arg_exists = expected_type is not None
        arg_type_matches = isinstance(value, expected_type)
        if ex_arg_exists and not arg_type_matches:
            raise ArgError(
                f"Expected argument {arg_idx} to be of type {expected_type}, got {type(value)}")

        return True

    def _add_command(self, name: str, func: Callable) -> None:
        pass
