from __future__ import annotations

import dataclasses
from typing import Sequence, Union, Optional, Any


@dataclasses.dataclass
class PassResult:
    test_name: str
    _: dataclasses.KW_ONLY
    sub_results: Sequence[PassResult] = dataclasses.field(default_factory=list)

    def __repr__(self) -> str:
        args = [repr(self.test_name)]
        if self.sub_results:
            args.append(f"sub_results={repr(self.sub_results)}")
        joined_args = ", ".join(args)
        return f"PassResult({joined_args})"


@dataclasses.dataclass
class FailResult:
    test_name: str
    _: dataclasses.KW_ONLY
    messages: list[str] = dataclasses.field(default_factory=list)
    sub_results: Sequence[Union[PassResult, FailResult]] = dataclasses.field(default_factory=list)

    def __repr__(self) -> str:
        args = [repr(self.test_name)]
        if self.messages:
            args.append(f"messages={repr(self.messages)}")
        if self.sub_results:
            args.append(f"sub_results={repr(self.sub_results)}")
        joined_args = ", ".join(args)
        return f"FailResult({joined_args})"


@dataclasses.dataclass
class ErrorResult:
    test_name: str
    _: dataclasses.KW_ONLY
    error: Optional[Exception] = None
    sub_results: Sequence[Union[PassResult, FailResult, ErrorResult]] = dataclasses.field(
        default_factory=list
    )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ErrorResult):
            return False
        if self.test_name != other.test_name or self.sub_results != other.sub_results:
            return False
        if self.error and other.error:
            return self.error.args == other.error.args
        return not self.error and not other.error

    def __repr__(self) -> str:
        args = [repr(self.test_name)]
        if self.error:
            args.append(f"error={repr(self.error)}")
        if self.sub_results:
            args.append(f"sub_results={repr(self.sub_results)}")
        joined_args = ", ".join(args)
        return f"ErrorResult({joined_args})"


TestResult = Union[PassResult, FailResult, ErrorResult]
TestResults = Sequence[TestResult]
