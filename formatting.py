from running import TestResult


def format_friendly(results: list[TestResult]) -> str:
    """
    Returns the given test results in a human readable format.

    The format for each result is:
        $TEST_NAME (PASS | FAIL)
            [$FAILURE_MESSAGE]
    """
    lines = []
    for result in results:
        pass_fail = "PASS" if result.is_pass else "FAIL"
        lines.append(f"{result.test_name} {pass_fail}")
        if result.message:
            lines.append(f"    {result.message}")
    return "\n".join(lines)
