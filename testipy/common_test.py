from typing import Callable
import pathlib
import textwrap


def dedent(s: str) -> str:
    '''
    Dedent a multi-line string.

    Examples:
        >>> dedent(
        ...     """
        ...     line 1
        ...     line 2
        ...     """
        ... )
        "line 1\nline 2\n"
    '''
    return textwrap.dedent(s).lstrip()


def get_project_root() -> pathlib.Path:
    """
    Returns the absolute project root directory so that expected test ouptuts
    which reference file paths can be created.
    """
    common_test_path = pathlib.Path(__file__)
    # current path is $PROJECT_ROOT/testipy/common_test.py so need second parent
    return common_test_path.parents[1].absolute()


def def_line(f: Callable) -> int:
    """Returns the line that the given function was defined at."""
    return f.__code__.co_firstlineno
