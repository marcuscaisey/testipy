import dataclasses
from typing import Callable


@dataclasses.dataclass(order=False)
class TestResult:
    test_name: str
    is_pass: bool = True
    message: str = ""

    def _fail(self, message: str):
        self.is_pass = False
        self.message = message


class TestContext:
    def __init__(self, result: TestResult):
        self.result = result

    def fail(self, message: str = ""):
        self.result._fail(message)


TestFunction = Callable[[TestContext], None]


def run_test(test: TestFunction) -> TestResult:
    result = TestResult(test.__name__)
    t = TestContext(result)
    test(t)
    return t.result
