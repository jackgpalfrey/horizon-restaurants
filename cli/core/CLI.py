from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Evaluator import Evaluator


class Env:
    IS_ENV = True

    def __init__(self, evaluator: "Evaluator") -> None:
        self._evaluator = evaluator

    def include_library(self, library: str):
        """
        Imports the given library into the CLI.
        """

        self._evaluator.include(library)

    def reload_libraries(self):
        """
        Reloads all libraries that have been included into the evaluator.
        """

        self._evaluator.reload()

    def set_ctx(self, key: str, value: any):
        """
        Sets the context of the evaluator to the CLI.
        """

        self._evaluator.ctx[key] = value

    def get_ctx(self, key: str) -> any:
        """
        Gets the context of the evaluator.
        """

        return self._evaluator.ctx.get(key, None)

    def get_all_ctx(self) -> dict[str, any]:
        """
        Gets the context of the evaluator.
        """

        return self._evaluator.ctx

    def usage(self, cmd: str) -> str:
        """
        Returns usage information of given command
        """
        func = self._evaluator._commands.get(cmd, None)
        if func is None:
            return f"Command '{cmd}' not found."

        return self._evaluator._get_usage(func)[7:]  # Remove 'Usage: '

    def usage_all(self):
        """
        Returns usage information of all commands
        """
        usages = []
        for cmd in self._evaluator._commands:
            usages.append(self.usage(cmd))

        return usages

    def doc(self, cmd: str) -> str:
        """
        Returns documentation of given command
        """
        func = self._evaluator._commands.get(cmd, None)
        if func is None:
            return f"Command '{cmd}' not found."

        return func.__doc__
