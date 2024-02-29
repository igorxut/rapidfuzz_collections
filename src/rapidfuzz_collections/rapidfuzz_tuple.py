
from copy import (
    copy,
    deepcopy
)
from rapidfuzz.fuzz import WRatio
from rapidfuzz.process import (
    extract,
    extractOne,
    extract_iter
)
from typing import (
    Any,
    Generator,
    Iterator,
    Union
)

from .enums import (
    ScorerType,
    Strategy
)
from .types import (
    NormalizerProtocol,
    ScorerProtocol,
    ScorerResultListType
)
from .base import RapidfuzzCollection


# noinspection DuplicatedCode
class RapidFuzzTuple(RapidfuzzCollection):
    """
    Collection with fuzzy search functionality based on "tuple".
    """

    def __add__(self, value: Union['RapidFuzzTuple', tuple]) -> 'RapidFuzzTuple':
        """ Return self+value. """

        if isinstance(value, self.__class__):
            seq = self._data + value._data
        elif isinstance(value, tuple):
            seq = self._data + value
        else:
            raise TypeError(f"'+' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

        return self.__class__(
            seq,
            normalizer=self.normalizer,
            score_cutoff=self.default_score_cutoff,
            score_hint=self.default_score_hint,
            scorer=self.default_scorer,
            scorer_kwargs=self.default_scorer_kwargs,
            scorer_type=self.default_scorer_type,
            strategy=self.default_strategy
        )

    def __contains__(self, item: Any) -> bool:
        """ Return bool(key in self). """

        return item in self._data

    def __copy__(self) -> 'RapidFuzzTuple':
        """ Return shallow copy. """

        seq = copy(self._data)
        normalizer = copy(self.normalizer)

        return self.__class__(
            seq,
            normalizer=normalizer,
            score_cutoff=self.default_score_cutoff,
            score_hint=self.default_score_hint,
            scorer=self.default_scorer,
            scorer_kwargs=self.default_scorer_kwargs,
            scorer_type=self.default_scorer_type,
            strategy=self.default_strategy
        )

    def __deepcopy__(self, memodict) -> 'RapidFuzzTuple':
        """ Return deep copy. """

        seq = deepcopy(self._data, memo=memodict)
        normalizer = deepcopy(self.normalizer)

        return self.__class__(
            seq,
            normalizer=normalizer,
            score_cutoff=self.default_score_cutoff,
            score_hint=self.default_score_hint,
            scorer=self.default_scorer,
            scorer_kwargs=self.default_scorer_kwargs,
            scorer_type=self.default_scorer_type,
            strategy=self.default_strategy
        )

    def __eq__(self, value: Any) -> bool:
        """ Return self==value. """

        if not isinstance(value, self.__class__):
            return False

        return (
            self._data == value._data and
            self.choices == value.choices and
            self.default_score_cutoff == value.default_score_cutoff and
            self.default_score_hint == value.default_score_hint and
            self.default_scorer_type == value.default_scorer_type and
            self.default_strategy == value.default_strategy
        )

    def __getitem__(self, index: int) -> Any:
        """ Return self[index]. """

        return self._data[index]

    def __init__(
        self,
        *args,
        normalizer: NormalizerProtocol = None,
        score_cutoff: int | float | None = None,
        score_hint: int | float | None = None,
        scorer: ScorerProtocol = WRatio,
        scorer_kwargs: dict[str, Any] | None = None,
        scorer_type: ScorerType = ScorerType.SIMILARITY,
        strategy: Strategy = Strategy.FIRST_FROM_BEST
    ):
        """
        Immutable sequence. Basis is tuple.

        If no argument is given, the constructor returns an empty tuple.
        If iterable is specified the tuple is initialized from iterable's items.

        If the argument is a tuple, the return value is the same object.

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

        length = len(args)
        if length == 0:
            self._data = tuple()
        elif length == 1:
            self._data = tuple(args[0])
        else:
            raise TypeError(f"Need: 0 or 1 positional argument. Got: {length} positional arguments")

        self._choices = tuple()

        super().__init__(
            normalizer=normalizer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer=scorer,
            scorer_kwargs=scorer_kwargs,
            scorer_type=scorer_type,
            strategy=strategy
        )

    def __iter__(self) -> Iterator:
        """ Implement iter(self). """

        return iter(self._data)

    def __len__(self) -> int:
        """ Return len(self). """

        return len(self._data)

    def __mul__(self, value: int) -> 'RapidFuzzTuple':
        """ Implement self*value. """

        if not isinstance(value, int):
            raise TypeError(f"'*' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

        seq = self._data * value

        return self.__class__(
            seq,
            normalizer=self.normalizer,
            score_cutoff=self.default_score_cutoff,
            score_hint=self.default_score_hint,
            scorer=self.default_scorer,
            scorer_kwargs=self.default_scorer_kwargs,
            scorer_type=self.default_scorer_type,
            strategy=self.default_strategy
        )

    def __ne__(self, value: Any) -> bool:
        """ Return self!=value. """

        if not isinstance(value, self.__class__):
            return True

        return not (
            self._data == value._data and
            self.choices == value.choices and
            self.default_score_cutoff == value.default_score_cutoff and
            self.default_score_hint == value.default_score_hint and
            self.default_scorer_type == value.default_scorer_type and
            self.default_strategy == value.default_strategy
        )

    def __repr__(self) -> str:
        """ Return repr(self). """

        return f"{self.__class__.__qualname__}({repr(self._data)})"

    def __rmul__(self, value: int) -> 'RapidFuzzTuple':
        """ Implement value*self. """

        if not isinstance(value, int):
            raise TypeError(f"'*' not supported between instances of '{type(value)}' and '{self.__class__.__qualname__}'")  # noqa: E501

        seq = value * self._data

        return self.__class__(
            seq,
            normalizer=self.normalizer,
            score_cutoff=self.default_score_cutoff,
            score_hint=self.default_score_hint,
            scorer=self.default_scorer,
            scorer_kwargs=self.default_scorer_kwargs,
            scorer_type=self.default_scorer_type,
            strategy=self.default_strategy
        )

    @property
    def choices(self) -> tuple:
        return deepcopy(self._choices)

    def _normalize_choices(self):
        """
        Normalize all values of choices.
        """

        self._choices = tuple( self.normalizer(i) for i in self._data )

    def count(self, value: Any) -> int:
        """ Return number of occurrences of value. """

        return self._data.count(value)

    def index(self, value: Any, *args):
        """
        Return first index of value.

        Raises ValueError if the value is not present.
        """

        return self._data.index(value, *args)

    def fuzzy_contains(self, value: Any, **kwargs) -> bool:
        """
        Check for a similar value in the collection.

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

        :return:
        `True` if the similar value in the collection, `False` otherwise.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))
        scorer_type = self._check_scorer_type(kwargs.get('scorer_type', self.default_scorer_type))

        if self.__contains__(value):
            return True

        q = self.normalizer(value)

        if q is not None and q in self._choices:
            return True

        for choice, score, index in extract_iter(
            q,
            self._choices,
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs
        ):
            if (
                ( scorer_type == ScorerType.SIMILARITY and score > 0 ) or
                ( scorer_type == ScorerType.DISTANCE and score < ( len(q) + len(choice) ) )  # noqa
            ):
                return True
        return False

    def fuzzy_count(self, value: Any, **kwargs) -> int:
        """
        Based on standard `count` method, but use with fuzzy search.

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

        :return:
        Number of occurrences of value.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))
        scorer_type = self._check_scorer_type(kwargs.get('scorer_type', self.default_scorer_type))

        q = self.normalizer(value)

        counter = 0
        for choice, score, index in extract_iter(
            q,
            self._choices,
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs
        ):
            if (
                ( scorer_type == ScorerType.SIMILARITY and score > 0 ) or
                ( scorer_type == ScorerType.DISTANCE and score < ( len(q) + len(choice) ) )
            ):
                counter += 1

        return counter

    def fuzzy_get(self, value: Any, **kwargs) -> Any:
        """
        Return the element of collection which most similar to value.

        :param value:
        value to search for in collection's keys.

        :param kwargs:
        Optional named arguments:
            score_cutoff
            score_hint
            scorer
            scorer_kwargs
            scorer_type
            strategy
        If an argument is passed, then it is used for the search,
        otherwise the default value specified when the class was initialized is used.

        :return:
        The value from collection if exists a similar value, `None` otherwise.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))
        scorer_type = self._check_scorer_type(kwargs.get('scorer_type', self.default_scorer_type))
        strategy = self._check_strategy(kwargs.get('strategy', self.default_strategy))

        if self.__contains__(value):
            return value

        q = self.normalizer(value)

        if q is not None and q in self._choices:
            index = self._choices.index(q)
            return self.__getitem__(index)

        if strategy == Strategy.FIRST_FROM_BEST:
            result = extractOne(
                q,
                self._choices,
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs
            )
            if result is None:
                return None
            choice, score, index = result
            return self.__getitem__(index)

        elif strategy == Strategy.BEST_ONLY_ONE:
            result = extract(
                q,
                self._choices,
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs,
                limit=2
            )
            if not result:
                return None
            if len(result) == 1:
                choice, score, index = result[0]
                return self.__getitem__(index)
            return None

        elif strategy == Strategy.FIRST:
            for choice, score, index in extract_iter(
                q,
                self._choices,
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs
            ):
                if (
                    ( scorer_type == ScorerType.SIMILARITY and score > 0 ) or
                    ( scorer_type == ScorerType.DISTANCE and score < ( len(q) + len(choice) ) )  # noqa
                ):
                    return self.__getitem__(index)
            return None

        raise NotImplementedError

    def fuzzy_index(self, value: Any, **kwargs) -> int | None:
        """
        Based on standard `index` method, but use with fuzzy search.

        :param value:
        Value to search for in collection.

        :param kwargs:
        Optional named arguments:
            score_cutoff
            score_hint
            scorer
            scorer_kwargs
            scorer_type
            strategy
        If an argument is passed, then it is used for the search,
        otherwise the default value specified when the class was initialized is used.

        :return:
        Zero-based index in the list of the first item whose value is similar to value,
        or `None` if there are no similar values.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))
        scorer_type = self._check_scorer_type(kwargs.get('scorer_type', self.default_scorer_type))
        strategy = self._check_strategy(kwargs.get('strategy', self.default_strategy))

        if self.__contains__(value):
            return self.index(value)

        q = self.normalizer(value)

        if q is not None and q in self._choices:
            return self._choices.index(q)

        if strategy == Strategy.FIRST_FROM_BEST:
            result = extractOne(
                q,
                self._choices,
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs
            )
            if result is None:
                return None
            choice, score, index = result
            return index

        elif strategy == Strategy.BEST_ONLY_ONE:
            result = extract(
                q,
                self._choices,
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs,
                limit=2
            )
            if not result:
                return None
            if len(result) == 1:
                choice, score, index = result[0]
                return index
            return None

        elif strategy == Strategy.FIRST:
            for choice, score, index in extract_iter(
                q,
                self._choices,
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs
            ):
                if (
                    ( scorer_type == ScorerType.SIMILARITY and score > 0 ) or
                    ( scorer_type == ScorerType.DISTANCE and score < ( len(q) + len(choice) ) )  # noqa
                ):
                    return index
            return None

        raise NotImplementedError

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
        If an argument is passed, then it is used for the search,
        otherwise the default value specified when the class was initialized is used.

        :return:
        List of Tuples with 3 elements:
            The first element is element of collection, which is the value that’s compared to the query.
            The second value represents the similarity calculated by the scorer. This can be:
                - An edit distance (distance is 0 for a perfect match and > 0 for non-perfect matches).
                  In this case only choices which have a distance <= score_cutoff are returned.
                - A normalized edit distance (similarity is a score between 0 and 100, with 100 being a perfect match).
                  In this case only choices which have a similarity >= score_cutoff are returned.
                - `None` if normalized value is `None`
            The third parameter is the index of element.
        The list is sorted by similarity or distance depending on the scorer used.
        The first element in the list has the highest similarity / the smallest distance.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))

        q = self.normalizer(value)

        result = []
        indexes = set()

        for choice, score, index in extract(
            q,
            self._choices,
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs,
            limit=None
        ):
            item = self.__getitem__(index), score, index
            indexes.add(index)
            result.append(item)

        for index, value in enumerate(self):
            if index not in indexes:
                item = value, None, index
                result.append(item)

        return result

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
        If an argument is passed, then it is used for the search,
        otherwise the default value specified when the class was initialized is used.

        Yield tuple with 3 elements:
            The first element is element of collection, which is the value that’s compared to the query.
            The second value represents the similarity calculated by the scorer. This can be:
                - An edit distance (distance is 0 for a perfect match and > 0 for non-perfect matches).
                  In this case only choices which have a distance <= score_cutoff are returned.
                - A normalized edit distance (similarity is a score between 0 and 100, with 100 being a perfect match).
                  In this case only choices which have a similarity >= score_cutoff are returned.
            The third parameter is the index of element.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))

        q = self.normalizer(value)

        for choice, score, index in extract_iter(
            q,
            self._choices,
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs
        ):
            yield self.__getitem__(index), score, index
