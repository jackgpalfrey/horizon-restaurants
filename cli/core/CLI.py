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
