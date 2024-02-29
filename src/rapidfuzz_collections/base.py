
from rapidfuzz.fuzz import WRatio
from typing import (
    Any,
    Generator
)

from .enums import (
    ScorerType,
    Strategy
)
from .normatlization import Normalizer
from .types import (
    NormalizerProtocol,
    ScorerProtocol,
    ScorerResultListType
)


class RapidfuzzCollection:
    """
    Base class for extending the collection with fuzzy search functionality.
    """

    def __init__(
        self,
        normalizer: NormalizerProtocol = None,
        score_cutoff: int | float | None = None,
        score_hint: int | float | None = None,
        scorer: ScorerProtocol = WRatio,
        scorer_kwargs: dict[str, Any] | None = None,
        scorer_type: ScorerType = ScorerType.SIMILARITY,
        strategy: Strategy = Strategy.FIRST_FROM_BEST
    ):
        """
        :param normalizer:
        Callable for converting and normalization collections values/keys.

        :param score_cutoff:
        Optional argument for a score threshold. When an edit distance is used this represents the maximum
        edit distance and matches with a distance > score_cutoff are ignored. When a normalized edit distance is used
        this represents the minimal similarity and matches with a similarity < score_cutoff are ignored.
        `None` deactivates this behaviour.

        :param score_hint:
        Optional argument for an expected score to be passed to the scorer.
        This is used to select a faster implementation. `None` deactivates this behaviour.

        :param scorer:
        Callable that is used to calculate the matching score between the query and each choice from collection.
        This can be any of the scorers included in RapidFuzz (both scorers that calculate the edit distance or
        the normalized edit distance), or a custom function, which returns a normalized edit distance.

        :param scorer_kwargs:
        Any other named parameters are passed to the scorer.
        This can be used to pass e.g. weights to Levenshtein.distance.

        :param scorer_type:
        Type of Rapidfuzz Scorer. Interprets the evaluation score.

        :param strategy:
        Strategy for searching and returning values.
        """

        self._normalizer = None
        self._score_cutoff = None
        self._score_hint = None
        self._scorer = None
        self._scorer_kwargs = None
        self._scorer_type = None
        self._strategy = None

        self.normalizer = Normalizer.default() if normalizer is None else normalizer
        self.default_score_cutoff = score_cutoff
        self.default_score_hint = score_hint
        self.default_scorer = scorer
        self.default_scorer_kwargs = scorer_kwargs
        self.default_scorer_type = scorer_type
        self.default_strategy = strategy

    @property
    def normalizer(self) -> NormalizerProtocol:
        return self._normalizer

    @normalizer.setter
    def normalizer(self, normalizer: NormalizerProtocol):
        self._normalizer = self._check_normalizer(normalizer)
        self._normalize_choices()

    @property
    def default_score_cutoff(self) -> int | float | None:
        return self._score_cutoff

    @default_score_cutoff.setter
    def default_score_cutoff(self, value: int | float | None):
        self._score_cutoff = self._check_score_cutoff(value)

    @property
    def default_score_hint(self) -> int | float | None:
        return self._score_hint

    @default_score_hint.setter
    def default_score_hint(self, value: int | float | None):
        self._score_hint = self._check_score_hint(value)

    @property
    def default_scorer(self) -> ScorerProtocol:
        return self._scorer

    @default_scorer.setter
    def default_scorer(self, value: ScorerProtocol):
        self._scorer = self._check_scorer(value)

    @property
    def default_scorer_kwargs(self) -> dict[str, Any] | None:
        return self._scorer_kwargs

    @default_scorer_kwargs.setter
    def default_scorer_kwargs(self, value: dict[str, Any] | None = None):
        self._scorer_kwargs = self._check_scorer_kwargs(value)

    @property
    def default_scorer_type(self) -> ScorerType:
        return self._scorer_type

    @default_scorer_type.setter
    def default_scorer_type(self, value: ScorerType):
        self._scorer_type = self._check_scorer_type(value)

    @property
    def default_strategy(self) -> Strategy:
        return self._strategy

    @default_strategy.setter
    def default_strategy(self, value: Strategy):
        self._strategy = self._check_strategy(value)

    @staticmethod
    def _check_normalizer(value: NormalizerProtocol) -> NormalizerProtocol:
        if not callable(value):
            raise TypeError(f"normalizer=`{str(value)}` type=`{type(value)}` not supported")
        return value

    @staticmethod
    def _check_score_cutoff(value: int | float | None) -> int | float | None:
        if not (value is None or isinstance(value, ( int, float, ))):
            raise TypeError(f"Need: 'int' | 'float' | 'None'. Got: `{str(value)}` type=`{type(value)}`")
        return value

    @staticmethod
    def _check_score_hint(value: int | float | None) -> int | float | None:
        if not (value is None or isinstance(value, ( int, float, ))):
            raise TypeError(f"Need: 'int' | 'float' | 'None'. Got: `{str(value)}` type=`{type(value)}`")
        return value

    @staticmethod
    def _check_scorer(value: ScorerProtocol) -> ScorerProtocol:
        if not callable(value):
            raise TypeError(f"scorer=`{str(value)}` type=`{type(value)}` not supported")
        return value

    @staticmethod
    def _check_scorer_kwargs(value: dict[str, Any] | None) -> dict[str, Any] | None:
        if not (value is None or isinstance(value, dict)):
            raise TypeError(f"Need: `dict` | `None`. Got: `{str(value)}` type=`{type(value)}`")
        return value

    @staticmethod
    def _check_scorer_type(value: ScorerType) -> ScorerType:
        if not isinstance(value, ScorerType):
            raise TypeError(f"Need: `ScorerType`. Got: `{str(value)}` type=`{type(value)}`")
        return value

    @staticmethod
    def _check_strategy(value: Strategy) -> Strategy:
        if not isinstance(value, Strategy):
            raise TypeError(f"Need: `Strategy`. Got: `{str(value)}` type=`{type(value)}`")
        return value

    def fuzzy_contains(self, value: Any, **kwargs) -> bool:
        """
        Check for a similar value in the collection.

        :param value:
        Value to search for in collection.

        :return:
        `True` if the similar value in the collection, `False` otherwise.
        """
        ...

    def fuzzy_get(self, value: Any, **kwargs) -> Any:
        """
        Return the element of collection which most similar to value.

        :param value:
        Value to search for in collection.
        """
        ...

    def get_fuzzy_scores(self, value: Any, **kwargs) -> list[ScorerResultListType]:
        """
        Score all elements of the collection.

        :param value:
        Value to search for in collection.

        :param kwargs:
        Optional named arguments:
            score_cutoff
            score_hint
            scorer
            scorer_kwargs
            scorer_type
        If an argument is passed, then it is used for the search,
        otherwise the default value specified when the class was initialized is used.
        """
        ...

    def get_fuzzy_score_iter(self, value: Any, **kwargs) -> Generator[ScorerResultListType, None, None]:
        """
        Yields similarity between the query and each element of collection.
        If an element is normalized to `None`, then it is skipped.

        :param value:
        Value to search for in collection.

        :param kwargs:
        Optional named arguments:
            score_cutoff
            score_hint
            scorer
            scorer_kwargs
            scorer_type
        If an argument is passed, then it is used for the search,
        otherwise the default value specified when the class was initialized is used.
        """
        ...

    def _normalize_choices(self):
        """
        Normalize all values of choices.
        """

        raise NotImplementedError
