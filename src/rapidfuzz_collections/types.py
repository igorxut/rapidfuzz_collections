
from typing import (
    Any,
    Callable,
    Hashable,
    Protocol,
    Sequence
)


class NormalizerProtocol(Protocol):

    def __call__(self, value: Any) -> str | None:
        ...


class ScorerProtocol(Protocol):

    def __call__(self, s1: Sequence[Hashable] | None, s2: Sequence[Hashable] | None, **kwargs) -> float | int:
        ...


NormalizerOperationType = tuple[str, Callable, tuple, dict]
ScorerResultDictType = tuple[Any, float, Any]
ScorerResultListType = tuple[Any, float, int]
ScorerResultSetType = tuple[Any, float]
