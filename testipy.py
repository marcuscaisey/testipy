from typing import Callable


class TestResult:
    def __init__(self):
        self.is_pass = True
        self.message = ""

    def _fail(self, message: str):
        self.is_pass = False
        self.message = message


class TestContext:
    def __init__(self):
        self.result = TestResult()

    def fail(self, message: str = ""):
        self.result._fail(message)


TestFunction = Callable[[TestContext], None]


def run_test(test: TestFunction) -> TestResult:
    t = TestContext()
    test(t)
    return t.result
