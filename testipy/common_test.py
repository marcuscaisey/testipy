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
