import inspect
from typing import Iterable, Union

from .results import TestResults
from .functions import _run_test_function, TestFunction
from .classes import _run_test_class


def run_tests(tests: Iterable[Union[TestFunction, type]]) -> TestResults:
    """Runs some test functions and test classes and returns their result."""
    results: TestResults = []
    for test in tests:
        if inspect.isfunction(test):
            test_function = test
            result = _run_test_function(test_function)
            results.append(result)

        elif inspect.isclass(test):
            test_class = test
            result = _run_test_class(test_class)
            results.append(result)

    return results
