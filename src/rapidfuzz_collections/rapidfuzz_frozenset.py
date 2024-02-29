
from copy import copy
from rapidfuzz.fuzz import WRatio
from rapidfuzz.process import (
    extract,
    extractOne,
    extract_iter
)
from typing import (
    Any,
    Generator,
    Hashable,
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
    ScorerResultSetType
)
from .base import RapidfuzzCollection


# noinspection DuplicatedCode
class RapidFuzzFrozenSet(RapidfuzzCollection):
    """
    Collection with fuzzy search functionality based on "frozenset".
    """

    def __and__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return self&value. """

        if isinstance(value, self.__class__):
            seq = self._data & value._data
        elif isinstance(value, ( set, frozenset, )):
            seq = self._data & value
        else:
            raise TypeError(f"'&' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

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

    def __copy__(self) -> 'RapidFuzzFrozenSet':
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
        RapidFuzzFrozenSet() -> new empty RapidFuzzFrozenSet object
        RapidFuzzFrozenSet(iterable) -> new RapidFuzzFrozenSet object

        Build an immutable unordered collection of unique elements.
        """

        length = len(args)
        if length == 0:
            self._data = frozenset()
        elif length == 1:
            self._data = frozenset(args[0])
        else:
            raise TypeError(f"Need: 0 or 1 positional argument. Got: {length} positional arguments")

        self._choices = {}

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

    def __or__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return self|value. """

        if isinstance(value, self.__class__):
            seq = self._data | value._data
        elif isinstance(value, ( set, frozenset, )):
            seq = self._data | value
        else:
            raise TypeError(f"'|' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

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

    def __rand__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return value&self. """

        if isinstance(value, self.__class__):
            seq = value._data & self._data
        elif isinstance(value, ( set, frozenset, )):
            seq = value & self._data
        else:
            raise TypeError(f"'&' not supported between instances of '{type(value)}' and '{self.__class__.__qualname__}'")  # noqa: E501

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

    def __repr__(self) -> str:
        """ Return repr(self). """

        return f"{self.__class__.__qualname__}({repr(self._data)})"

    def __ror__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return value|self. """

        if isinstance(value, self.__class__):
            seq = value._data | self._data
        elif isinstance(value, ( set, frozenset, )):
            seq = value | self._data
        else:
            raise TypeError(f"'|' not supported between instances of '{type(value)}' and '{self.__class__.__qualname__}'")  # noqa: E501

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

    def __rsub__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return value-self. """

        if isinstance(value, self.__class__):
            seq = value._data - self._data
        elif isinstance(value, ( set, frozenset, )):
            seq = value - self._data
        else:
            raise TypeError(f"'-' not supported between instances of '{type(value)}' and '{self.__class__.__qualname__}'")  # noqa: E501

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

    def __rxor__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return value^self. """

        if isinstance(value, self.__class__):
            seq = value._data ^ self._data
        elif isinstance(value, ( set, frozenset, )):
            seq = value ^ self._data
        else:
            raise TypeError(f"'^' not supported between instances of '{type(value)}' and '{self.__class__.__qualname__}'")  # noqa: E501

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

    def __sub__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return self-value. """

        if isinstance(value, self.__class__):
            seq = self._data - value._data
        elif isinstance(value, ( set, frozenset, )):
            seq = self._data - value
        else:
            raise TypeError(f"'-' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

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

    def __xor__(self, value: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """ Return self^value. """

        if isinstance(value, self.__class__):
            seq = self._data ^ value._data
        elif isinstance(value, ( set, frozenset, )):
            seq = self._data ^ value
        else:
            raise TypeError(f"'^' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

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
    def choices(self) -> dict[str | None, set[Union[Hashable, None]]]:
        return self._choices

    def _normalize_choices(self):
        """
        Normalize all values of choices.
        """

        self._choices = {}
        for value in self:
            choice = self.normalizer(value)
            if choice not in self._choices:
                self._choices[choice] = set()
            self._choices[choice].add(value)

    def copy(self) -> 'RapidFuzzFrozenSet':
        """ Return a shallow copy. """

        seq = self._data.copy()
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

    def difference(self, *args) -> 'RapidFuzzFrozenSet':
        """
        Return the difference of 'RapidFuzzFrozenSet' and two or more 'RapidFuzzFrozenSet'
        or set as new 'RapidFuzzFrozenSet'.

        (i.e. all elements that are in this 'RapidFuzzFrozenSet' but not the others.)
        """

        sets = []

        for i in args:
            if isinstance(i, ( set, frozenset, )):
                sets.append(i)
            elif isinstance(i, self.__class__):
                sets.append(i._data)
            else:
                raise TypeError(f"'difference' not supported between instances of '{self.__class__.__qualname__}' and '{type(i)}'")  # noqa: E501

        seq = self._data.difference(*sets)

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

    def intersection(self, *args) -> 'RapidFuzzFrozenSet':
        """
        Return the intersection of 'RapidFuzzFrozenSet' and two or more 'RapidFuzzFrozenSet'
        or set as new 'RapidFuzzFrozenSet'.

        (i.e. all elements that are in both collections.)
        """

        sets = []

        for i in args:
            if isinstance(i, ( set, frozenset, )):
                sets.append(i)
            elif isinstance(i, self.__class__):
                sets.append(i._data)
            else:
                raise TypeError(f"'intersection' not supported between instances of '{self.__class__.__qualname__}' and '{type(i)}'")  # noqa: E501

        seq = self._data.intersection(*sets)

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

    def isdisjoint(self, other: Union['RapidFuzzFrozenSet', set, frozenset]) -> bool:
        """ Return True if two sets have a null intersection. """

        if isinstance(other, self.__class__):
            return self._data.isdisjoint(other._data)

        if isinstance(other, ( set, frozenset, )):
            return self._data.isdisjoint(other)

        raise TypeError(f"'isdisjoint' not supported between instances of '{self.__class__.__qualname__}' and '{type(other)}'")  # noqa: E501

    def issubset(self, other: Union['RapidFuzzFrozenSet', set, frozenset]) -> bool:
        """ Report whether another set contains this collection. """

        if isinstance(other, self.__class__):
            return self._data.issubset(other._data)

        if isinstance(other, ( set, frozenset, )):
            return self._data.issubset(other)

        raise TypeError(f"'issubset' not supported between instances of '{self.__class__.__qualname__}' and '{type(other)}'")  # noqa: E501

    def issuperset(self, other: Union['RapidFuzzFrozenSet', set, frozenset]) -> bool:
        """ Report whether this set contains another set. """

        if isinstance(other, self.__class__):
            return self._data.issuperset(other._data)

        if isinstance(other, ( set, frozenset, )):
            return self._data.issuperset(other)

        raise TypeError(f"'issuperset' not supported between instances of '{self.__class__.__qualname__}' and '{type(other)}'")  # noqa: E501

    def symmetric_difference(self, other: Union['RapidFuzzFrozenSet', set, frozenset]) -> 'RapidFuzzFrozenSet':
        """
        Return the symmetric difference of 'RapidFuzzFrozenSet' and 'RapidFuzzFrozenSet'
        or set as new 'RapidFuzzFrozenSet'.

        (i.e. all elements that are in exactly one of the sets.)
        """

        if isinstance(other, ( set, frozenset, )):
            seq = self._data.symmetric_difference(other)
        elif isinstance(other, self.__class__):
            seq = self._data.symmetric_difference(other._data)
        else:
            raise TypeError(f"'symmetric_difference' not supported between instances of '{self.__class__.__qualname__}' and '{type(other)}'")  # noqa: E501

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

    def union(self, *args) -> 'RapidFuzzFrozenSet':
        """
        Return the union of RapidFuzzFrozenSet and sets as a new RapidFuzzFrozenSet.

        (i.e. all elements that are in either set.)
        """

        sets = []

        for i in args:
            if isinstance(i, ( set, frozenset, )):
                sets.append(i)
            elif isinstance(i, self.__class__):
                sets.append(i._data)
            else:
                raise TypeError(f"'union' not supported between instances of '{self.__class__.__qualname__}' and '{type(i)}'")  # noqa: E501

        seq = self._data.union(*sets)

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

        for nk, score, index in extract_iter(
            q,
            self._choices.keys(),
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs
        ):
            if (
                ( scorer_type == ScorerType.SIMILARITY and score > 0 ) or
                ( scorer_type == ScorerType.DISTANCE and score < ( len(q) + len(nk) ) )  # noqa
            ):
                return True
        return False

    def fuzzy_get(self, value: Any, **kwargs) -> tuple | None:
        """
        Return the element of collection which most similar to value.

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
            ks = self._choices[q]
            if strategy == Strategy.BEST_ONLY_ONE:
                if len(ks) == 1:
                    k = next(iter(ks))
                    return k
            else:
                k = next(iter(ks))
                return k

        if strategy == Strategy.FIRST_FROM_BEST:
            result = extractOne(
                q,
                self._choices.keys(),
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs
            )
            if result is None:
                return None
            nk, score, index = result
            ks = self._choices[nk]
            k = next(iter(ks))
            return k

        elif strategy == Strategy.BEST_ONLY_ONE:
            result = extract(
                q,
                self._choices.keys(),
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs,
                limit=2
            )
            if not result:
                return None
            if len(result) == 1:
                nk, score, index = result[0]
                ks = self._choices[nk]
                if len(ks) == 1:
                    k = next(iter(ks))
                    return k
            return None

        elif strategy == Strategy.FIRST:
            for nk, score, index in extract_iter(
                q,
                self._choices.keys(),
                scorer=scorer,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                scorer_kwargs=scorer_kwargs
            ):
                if (
                    ( scorer_type == ScorerType.SIMILARITY and score > 0 ) or
                    ( scorer_type == ScorerType.DISTANCE and score < ( len(q) + len(nk) ) )
                ):
                    ks = self._choices[nk]
                    k = next(iter(ks))
                    return k
            return None

        raise NotImplementedError

    def get_fuzzy_scores(self, value: Any, **kwargs) -> list[ScorerResultSetType]:
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
        List of Tuples with 2 elements:
            The first element is element of collection.
            The second element represents the similarity calculated by the scorer. This can be:
                - An edit distance (distance is 0 for a perfect match and > 0 for non-perfect matches).
                  In this case only choices which have a distance <= score_cutoff are returned.
                - A normalized edit distance (similarity is a score between 0 and 100, with 100 being a perfect match).
                  In this case only choices which have a similarity >= score_cutoff are returned.
                - `None` if normalized value is `None`
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

        for nk, score, index in extract(
            q,
            self._choices.keys(),
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs,
            limit=None
        ):
            ks = self._choices[nk]
            for k in ks:
                item = k, score
                indexes.add(k)
                result.append(item)

        for k in self:
            if k not in indexes:
                item = k, None
                result.append(item)

        return result

    def get_fuzzy_score_iter(self, value: Any, **kwargs) -> Generator[ScorerResultSetType, None, None]:
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

        Yield tuple with 2 elements:
            The first element is element of collection.
            The second value represents the similarity calculated by the scorer. This can be:
                - An edit distance (distance is 0 for a perfect match and > 0 for non-perfect matches).
                  In this case only choices which have a distance <= score_cutoff are returned.
                - A normalized edit distance (similarity is a score between 0 and 100, with 100 being a perfect match).
                  In this case only choices which have a similarity >= score_cutoff are returned.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))

        q = self.normalizer(value)

        for nk, score, index in extract_iter(
            q,
            self._choices.keys(),
            scorer=scorer,
            score_cutoff=score_cutoff,
            score_hint=score_hint,
            scorer_kwargs=scorer_kwargs
        ):
            ks = self._choices[nk]
            for k in ks:
                yield k, score
