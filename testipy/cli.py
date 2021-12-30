import sys
from typing import TextIO

from .discovery import discover_tests
from .running import run_tests
from .formatting import format_friendly


def testipy(path: str, out: TextIO):
    """Run the tests at the given path, outputting the results"""
    tests = discover_tests(path)
    results = run_tests(tests)
    formatted_results = format_friendly(results)
    out.write(formatted_results)


def main(path):
    testipy(path, sys.stdout)
