import importlib
import inspect
from typing import Any, Callable, Union

from .running import TestFunction, TestContext


def discover_tests(path: str) -> list[Union[TestFunction, type]]:
    """
    Return the test functions and test classes found at the given path, sorted by order of
    definition.

    Definitions:
        Test Function
            Function which starts with 'test_' accepts a single TestContext argument.
        Test Class
            Class which starts with 'Test' and has at least one test method.
        Test Method
            Method which starts with 'test_' and accepts a single TestContext argument.

    Test functions / classes which are defined in modules other than the one at the given path are
    ignored.
    """
    module_name = path.replace("/", ".").removesuffix(".py")
    module = importlib.import_module(module_name)
    tests = [
        member
        for _, member in inspect.getmembers(module, predicate=_is_test_function_or_test_class)
    ]
    test_defined_in_module = filter(_defined_in_module(module_name), tests)
    return sorted(test_defined_in_module, key=_definition_line)


def _is_test_function_or_test_class(obj: Any) -> bool:
    return _is_test_function(obj) or _is_test_class(obj)


def _is_test_function(obj: Any) -> bool:
    if not inspect.isfunction(obj):
        return False
    if not obj.__name__.startswith("test_"):
        return False

    sig = inspect.signature(obj)
    if len(sig.parameters) != 1:
        return False

    test_context_param = list(sig.parameters.values())[0]
    return test_context_param.annotation == TestContext


def _is_test_class(obj: Any) -> bool:
    return inspect.isclass(obj) and obj.__name__.startswith("Test") and _has_test_method(obj)


def _has_test_method(obj: type) -> bool:
    # Use isfunction instead of ismethod because the functions defined on the class only become
    # "methods" when you access them on an instance of the class and they get bound to that
    # instance.
    for _, method in inspect.getmembers(obj, predicate=inspect.isfunction):
        if _is_test_method(method):
            return True
    return False


# TODO: this is used in running as well, make both modules use the same func?
def _is_test_method(value: Any) -> bool:
    if not inspect.isfunction(value):
        return False
    if not value.__name__.startswith("test_"):
        return False

    sig = inspect.signature(value)
    # should have self and TestContext parameters
    if len(sig.parameters) != 2:
        return False

    parameter = list(sig.parameters.values())[1]
    return parameter.annotation == TestContext


def _definition_line(obj: Any) -> int:
    _, definition_line = inspect.findsource(obj)
    return definition_line


# TODO: the usage of this is not obvious, should name it better
def _defined_in_module(name: str) -> Callable[[Callable], bool]:
    return lambda f: f.__module__ == name
