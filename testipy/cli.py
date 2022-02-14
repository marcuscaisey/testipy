import sys
from typing import Iterable, TextIO

from .discovery import discover_tests
from .running import run_tests
from .printing import FriendlyPrinter


def testipy(paths: Iterable[str], out: TextIO):
    """Run the tests at the given path, outputting the results"""
    tests = []
    for path in paths:
        tests.extend(discover_tests(path))
    results = run_tests(tests)
    printer = FriendlyPrinter(results)
    printer.print(out=out)


def main(paths: Iterable[str]):
    testipy(paths, sys.stdout)
