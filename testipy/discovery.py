import importlib
import inspect
from typing import Any, Callable

from .running import TestFunction, TestContext


def discover_tests(path: str) -> list[TestFunction]:
    """
    Return the test functions found at the given path, sorted by order of
    definition.

    A test function is one which:
        - accepts a TestContext as a single argument
        - begins with test_

    Test functions which are defined in modules other than the one at the given
    path are ignored.
    """
    module_name = path.replace("/", ".").removesuffix(".py")
    module = importlib.import_module(module_name)
    tests = [value for _, value in inspect.getmembers(module, _is_test_function)]
    tests = filter(_defined_in_module(module_name), tests)
    return sorted(tests, key=_definition_line)


def _is_test_function(value: Any) -> bool:
    if not inspect.isfunction(value):
        return False
    if not value.__name__.startswith("test_"):
        return False

    sig = inspect.signature(value)
    if len(sig.parameters) != 1:
        return False

    parameter = list(sig.parameters.values())[0]
    return parameter.annotation == TestContext


def _definition_line(f: Callable) -> int:
    return f.__code__.co_firstlineno


def _defined_in_module(name: str) -> Callable[[Callable], bool]:
    return lambda f: f.__module__ == name
