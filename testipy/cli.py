import sys
from typing import TextIO

from .discovery import discover_tests
from .running import run_tests
from .printing import FriendlyPrinter


def testipy(path: str, out: TextIO):
    """Run the tests at the given path, outputting the results"""
    tests = discover_tests(path)
    results = run_tests(tests)
    printer = FriendlyPrinter(results)
    printer.print(out=out)


def main(path):
    testipy(path, sys.stdout)
