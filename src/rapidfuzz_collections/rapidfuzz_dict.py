
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
    Self,
    Union
)

from .enums import (
    ScorerType,
    Strategy
)
from .types import (
    NormalizerProtocol,
    ScorerProtocol,
    ScorerResultDictType
)
from .base import RapidfuzzCollection


# noinspection DuplicatedCode
class RapidFuzzDict(RapidfuzzCollection):
    """
    Collection with fuzzy search functionality based on "dict".
    """

    def __contains__(self, item: Any) -> bool:
        """ Return bool(key in self). """

        return item in self._data

    def __copy__(self) -> 'RapidFuzzDict':
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

    def __deepcopy__(self, memodict) -> 'RapidFuzzDict':
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

    def __delitem__(self, key: Any):
        """ Delete self[key]. """

        del self._data[key]

        nk = self.normalizer(key)
        self._choices[nk].discard(key)
        if not self._choices[nk]:
            del self._choices[nk]

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

    def __getitem__(self, key: Any) -> Any:
        """ Return self[key]. """

        return self._data[key]

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
        RapidFuzzDict() -> new empty RapidFuzzDict
        RapidFuzzDict(mapping) -> new RapidFuzzDict initialized from a mapping object's
            (key, value) pairs
        RapidFuzzDict(iterable) -> new RapidFuzzDict initialized as if via:
            d = { k: v for k, v in iterable }
        """

        length = len(args)
        if length == 0:
            self._data = {}
        elif length == 1:
            self._data = dict(args[0])
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

    def __ior__(self, value: Union['RapidFuzzDict', dict]) -> Self:
        """ Return self|=value. """

        if isinstance(value, self.__class__):
            self._data |= value._data
        elif isinstance(value, dict):
            self._data |= value
        else:
            raise TypeError(f"'|=' not supported between instances of '{self.__class__.__qualname__}' and '{type(value)}'")  # noqa: E501

        self._normalize_choices()

        return self

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

    def __or__(self, value: Union['RapidFuzzDict', dict]) -> 'RapidFuzzDict':
        """ Return self|value. """

        if isinstance(value, self.__class__):
            seq = self._data | value._data
        elif isinstance(value, dict):
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

    def __repr__(self) -> str:
        """ Return repr(self). """

        return f"{self.__class__.__qualname__}({repr(self._data)})"

    def __reversed__(self) -> Iterator:
        """ Return a reverse iterator. """

        return reversed(self._data)

    def __ror__(self, value: Union['RapidFuzzDict', dict]) -> 'RapidFuzzDict':
        """ Return value|self. """

        if isinstance(value, self.__class__):
            seq = value._data | self._data
        elif isinstance(value, dict):
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

    def __setitem__(self, key: Any, value: Any):
        """ Set self[key] to value. """

        self._data[key] = value

        nk = self.normalizer(key)
        if nk not in self._choices:
            self._choices[nk] = set()
        self._choices[nk].add(key)

    @property
    def choices(self) -> dict[str | None, set[Any]]:
        return deepcopy(self._choices)

    def _normalize_choices(self):
        """
        Normalize all values of choices.
        """

        self._choices = {}
        for k in self._data.keys():
            nk = self.normalizer(k)
            if nk not in self._choices:
                self._choices[nk] = set()
            self._choices[nk].add(k)

    def clear(self):
        """ Remove all items from collection. """

        self._data.clear()
        self._choices.clear()

    def copy(self) -> 'RapidFuzzDict':
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

    @staticmethod
    def fromkeys(*args, **kwargs) -> 'RapidFuzzDict':
        """ Create a new RapidFuzzDict with keys from iterable and values set to value. """

        seq = dict.fromkeys(*args, **kwargs)
        return RapidFuzzDict(seq)

    def get(self, key: Any, default: Any = None) -> Any:
        """ Return the value for key if key is in the collection, else default. """

        return self._data.get(key, default)

    # noinspection PyUnresolvedReferences
    def items(self) -> 'dict_items':
        """ D.items() -> a set-like object providing a view on D's items """

        return self._data.items()

    # noinspection PyUnresolvedReferences
    def keys(self) -> 'dict_keys':
        """ D.keys() -> a set-like object providing a view on D's keys """

        return self._data.keys()

    def pop(self, key: Any, *args) -> Any:
        """
        pop(key[,default]) -> v, remove specified key and return the corresponding value.

        If the key is not found, return the default if given; otherwise,
        raise a KeyError.
        """

        length = len(args)
        if length > 1:
            TypeError(f"pop expected at least 1 argument and at most 2 arguments, got: {length}")

        is_exist = self.__contains__(key)
        value = self._data.pop(key, *args)
        if is_exist:
            nk = self.normalizer(key)
            if nk in self._choices:
                self._choices[nk].discard(key)
                if not self._choices[nk]:
                    del self._choices[nk]
        return value

    def popitem(self) -> tuple[str | None, Any]:
        """
        Remove and return a (key, value) pair as a 2-tuple.

        Pairs are returned in LIFO (last-in, first-out) order.
        Raises KeyError if the dict is empty.
        """

        k, v = self._data.popitem()
        nk = self.normalizer(k)
        if nk in self._choices:
            self._choices[nk].discard(k)
            if not self._choices[nk]:
                del self._choices[nk]
        return k, v

    def setdefault(self, key: Any, value: Any = None) -> Any:
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """

        if self.__contains__(key):
            return self._data[key]

        self._data[key] = value
        nk = self.normalizer(key)
        if nk not in self._choices:
            self._choices[nk] = set()
        self._choices[nk].add(key)

        return value

    def update(self, *args, **kwargs):
        """
        update([E, ]**F) -> None. Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """

        self._data.update(*args, **kwargs)
        self._normalize_choices()

    # noinspection PyUnresolvedReferences
    def values(self) -> 'dict_values':
        """ an object providing a view on D's values """

        return self._data.values()

    def fuzzy_contains(self, key: Any, **kwargs) -> bool:
        """
        Check for a similar key in the collection.

        :param key:
        Key to search for in collection's keys.

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
        `True` if the similar key in the collection, `False` otherwise.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))
        scorer_type = self._check_scorer_type(kwargs.get('scorer_type', self.default_scorer_type))

        if self.__contains__(key):
            return True

        q = self.normalizer(key)

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

    def fuzzy_get(self, key: Any, **kwargs) -> tuple | None:
        """
        Return the pair of key and value from collection with using fuzzy search by key.

        :param key:
        Key to search for in collection's keys.

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
        Tuple of key and value from collection if key exists, `None` otherwise.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))
        scorer_type = self._check_scorer_type(kwargs.get('scorer_type', self.default_scorer_type))
        strategy = self._check_strategy(kwargs.get('strategy', self.default_strategy))

        if self.__contains__(key):
            return key, self.__getitem__(key)

        q = self.normalizer(key)

        if q is not None and q in self._choices:
            ks = self._choices[q]
            if strategy == Strategy.BEST_ONLY_ONE:
                if len(ks) == 1:
                    k = next(iter(ks))
                    return k, self.__getitem__(k)
            else:
                k = next(iter(ks))
                return k, self.__getitem__(k)

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
            return k, self.__getitem__(k)

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
                    return k, self.__getitem__(k)
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
                    return k, self.__getitem__(k)
            return None

        raise NotImplementedError

    def get_fuzzy_scores(self, key: Any, **kwargs) -> list[ScorerResultDictType]:
        """
        Score all keys of the collection.

        :param key:
        Key to search for in collection's keys.

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
            The first element is the value of collection's element.
            The second element represents the similarity calculated by the scorer. This can be:
                - An edit distance (distance is 0 for a perfect match and > 0 for non-perfect matches).
                  In this case only choices which have a distance <= score_cutoff are returned.
                - A normalized edit distance (similarity is a score between 0 and 100, with 100 being a perfect match).
                  In this case only choices which have a similarity >= score_cutoff are returned.
                - `None` if normalized value is `None`
            The third parameter is the key of collection's element.
        The list is sorted by similarity or distance depending on the scorer used.
        The first element in the list has the highest similarity / the smallest distance.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))

        q = self.normalizer(key)

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
                item = self.__getitem__(k), score, k
                indexes.add(k)
                result.append(item)

        for k, v in self.items():
            if k not in indexes:
                item = v, None, k
                result.append(item)

        return result

    def get_fuzzy_score_iter(self, key: Any, **kwargs) -> Generator[ScorerResultDictType, None, None]:
        """
        Yields similarity between the query and each element of collection.
        If an element is normalized to `None`, then it is skipped.

        :param key:
        Key to search for in collection's keys.

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
            The third parameter is the key of collection's element.
        """

        score_cutoff = self._check_score_cutoff(kwargs.get('score_cutoff', self.default_score_cutoff))
        score_hint = self._check_score_hint(kwargs.get('score_hint', self.default_score_hint))
        scorer = self._check_scorer(kwargs.get('scorer', self.default_scorer))
        scorer_kwargs = self._check_scorer_kwargs(kwargs.get('scorer_kwargs', self.default_scorer_kwargs))

        q = self.normalizer(key)

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
                yield self.__getitem__(k), score, k
