from __future__ import annotations

import os
from types import TracebackType
from typing import Any


class MockFileLock:
    def __init__(self, lock_file: str | os.PathLike[Any], timeout: float = -1) -> None:
        print("MOCK")
        pass

    def __enter__(self) -> MockFileLock:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,  # noqa: U100
        exc_value: BaseException | None,  # noqa: U100
        traceback: TracebackType | None,  # noqa: U100
    ) -> None:
        pass

    def __del__(self) -> None:
        pass
