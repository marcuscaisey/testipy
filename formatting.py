from running import TestResult


def format_for_cli(results: list[TestResult]) -> str:
    lines = []
    for result in results:
        pass_fail = "PASS" if result.is_pass else "FAIL"
        lines.append(f"{result.test_name} {pass_fail}")
        if result.message:
            lines.append(f"    {result.message}")
    return "\n".join(lines)
