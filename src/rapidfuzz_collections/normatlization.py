
from copy import (
    copy,
    deepcopy
)
from re import (
    RegexFlag,
    sub
)
from typing import (
    Any,
    Callable,
    Match,
    Optional,
    Pattern,
    Self
)

from .types import NormalizerOperationType


# noinspection DuplicatedCode
class Normalizer:
    """
    Utility for converting and normalization collections values/keys.
    """

    _MAPPING = {
        'capitalize': lambda v, args, kwargs: v.capitalize() if isinstance(v, str) else None,
        'casefold': lambda v, args, kwargs: v.casefold() if isinstance(v, str) else None,
        'endswith': lambda v, args, kwargs: ( v if v.endswith(*args) else None ) if isinstance(v, str) else None,
        'exact_length': lambda v, args, kwargs: ( v if len(v) == args[0] else None ) if isinstance(v, str) else None,
        'isalnum': lambda v, args, kwargs: ( v if v.isalnum() else None ) if isinstance(v, str) else None,
        'isalpha': lambda v, args, kwargs: ( v if v.isalpha() else None ) if isinstance(v, str) else None,
        'isascii': lambda v, args, kwargs: ( v if v.isascii() else None ) if isinstance(v, str) else None,
        'isdecimal': lambda v, args, kwargs: ( v if v.isdecimal() else None ) if isinstance(v, str) else None,
        'isdigit': lambda v, args, kwargs: ( v if v.isdigit() else None ) if isinstance(v, str) else None,
        'isidentifier': lambda v, args, kwargs: ( v if v.isidentifier() else None ) if isinstance(v, str) else None,
        'isinstance_str': lambda v, args, kwargs: v if isinstance(v, str) else None,
        'islower': lambda v, args, kwargs: ( v if v.islower() else None ) if isinstance(v, str) else None,
        'isnumeric': lambda v, args, kwargs: ( v if v.isnumeric() else None ) if isinstance(v, str) else None,
        'isprintable': lambda v, args, kwargs: ( v if v.isprintable() else None ) if isinstance(v, str) else None,
        'isspace': lambda v, args, kwargs: ( v if v.isspace() else None ) if isinstance(v, str) else None,
        'istitle': lambda v, args, kwargs: ( v if v.istitle() else None ) if isinstance(v, str) else None,
        'isupper': lambda v, args, kwargs: ( v if v.isupper() else None ) if isinstance(v, str) else None,
        'lower': lambda v, args, kwargs: v.lower() if isinstance(v, str) else None,
        'lstrip': lambda v, args, kwargs: v.lstrip(*args) if isinstance(v, str) else None,
        'max_length': lambda v, args, kwargs: ( v if len(v) <= args[0] else None ) if isinstance(v, str) else None,
        'min_length': lambda v, args, kwargs: ( v if len(v) >= args[0] else None ) if isinstance(v, str) else None,
        'not_empty_str': lambda v, args, kwargs: v if len(v) else None,
        're_sub': lambda v, args, kwargs: sub(args[0], args[1], v),
        'removeprefix': lambda v, args, kwargs: v.removeprefix(args[0]) if isinstance(v, str) else None,
        'removesuffix': lambda v, args, kwargs: v.removesuffix(args[0]) if isinstance(v, str) else None,
        'replace': lambda v, args, kwargs: v.replace(*args) if isinstance(v, str) else None,
        'rstrip': lambda v, args, kwargs: v.rstrip(*args) if isinstance(v, str) else None,
        'startswith': lambda v, args, kwargs: ( v if v.startswith(*args) else None ) if isinstance(v, str) else None,
        'strip': lambda v, args, kwargs: v.strip(*args) if isinstance(v, str) else None,
        'upper': lambda v, args, kwargs: v.upper() if isinstance(v, str) else None,
    }

    def __call__(self, value: Any) -> Optional[str]:
        """
        :param value: Value for normalization.
        :return: Normalized value.
        """
        _value = value

        for name, func, args, kwargs in self.operations:
            _value = func(_value, args, kwargs)

        if _value is not None and not isinstance(_value, str):
            raise ValueError(f"Need: `None` or `str`. Got: value=`{str(_value)}` type=`{type(_value)}`")

        return _value

    def __copy__(self) -> 'Normalizer':
        """ Return shallow copy. """

        instance = self.__new__(self.__class__)
        instance.__dict__['_operations'] = copy(self._operations)
        return instance

    def __deepcopy__(self, memodict) -> 'Normalizer':
        """ Return deep copy. """

        instance = self.__new__(self.__class__)
        instance.__dict__['_operations'] = deepcopy(self._operations)
        return instance

    def __init__(self):
        self._operations: list[NormalizerOperationType] = []

    @property
    def operations(self) -> tuple[NormalizerOperationType, ...]:
        return tuple(self._operations)

    @classmethod
    def default(cls) -> 'Normalizer':
        return cls().isinstance_str().strip().min_length(3)

    def capitalize(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.capitalize

        If type of value is `str` - modify and return. Else - `None`.
        """

        name = 'capitalize'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def casefold(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.casefold

        If type of value is `str` - modify and return. Else - `None`.
        """

        name = 'casefold'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def custom(self, func: Callable, *args, **kwargs) -> Self:

        if not callable(func):
            raise TypeError(f"Need: `Callable`. Got: `{str(func)}` type=`{type(func)}`")

        operation = ( 'custom', func, args, kwargs, )
        self._operations.append(operation)

        return self

    def endswith(self, *args) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.endswith

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        length = len(args)
        if length == 1:
            suffix, start, end = args[0], None, None
        elif length == 2:
            suffix, start, end = args[0], args[1], None
        elif length == 3:
            suffix, start, end = args[0], args[1], args[2]
        else:
            raise TypeError(f"Need: at least 1 argument, at most 3 argument. Got: {length} arguments")

        if isinstance(suffix, tuple):
            for _suffix in suffix:
                if not isinstance(_suffix, str):
                    raise TypeError(f"Need: `str`. Got: `{str(_suffix)}` type=`{type(_suffix)}`")
        elif not isinstance(suffix, ( str, tuple, )):
            raise TypeError(f"Need: `str` or `tuple[str]`. Got: `{str(suffix)}` type=`{type(suffix)}`")

        if start is not None and not isinstance(start, int):
            raise TypeError(f"Need: `int`. Got: {str(start)} type=`{type(start)}`")

        if end is not None and not isinstance(end, int):
            raise TypeError(f"Need: `int`. Got: `{str(end)}` type=`{type(end)}`")

        name = 'endswith'
        func = self._MAPPING[name]
        args = tuple( i for i in ( suffix, start, end, ) if i is not None )

        operation = ( name, func, args, {}, )
        self._operations.append(operation)

        return self

    def exact_length(self, length: int) -> Self:
        """
        Return value if type is `str` and length of the string is equal `length`. Else - `None`.

        :param length: length of the string.
        """

        if not isinstance(length, int):
            raise TypeError(f"Need: `int`. Got: `{str(length)}` type=`{type(length)}`")

        if length < 1:
            raise ValueError(f"Need: value greater than 0. Got: `{length}`")

        name = 'exact_length'
        func = self._MAPPING[name]

        operation = ( name, func, ( length, ), {}, )
        self._operations.append(operation)

        return self

    def isalnum(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isalnum

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isalnum'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isalpha(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isalpha

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isalpha'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isascii(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isascii

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isascii'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isdecimal(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isdecimal

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isdecimal'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isdigit(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isdigit

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isdigit'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isidentifier(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isidentifier

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isidentifier'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isinstance_str(self) -> Self:
        """
        Return value if type is `str`, else - `None`.
        """

        name = 'isinstance_str'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def islower(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.islower

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'islower'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isnumeric(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isnumeric

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isnumeric'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isprintable(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isprintable

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isprintable'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isspace(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isspace

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isspace'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def istitle(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.istitle

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'istitle'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def isupper(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.isupper

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        name = 'isupper'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def lower(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.lower

        If type of value is `str` - modify and return. Else - `None`.
        """

        name = 'lower'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def lstrip(self, *args) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.lstrip

        If type of value is `str` - modify and return. Else - `None`.
        """

        length = len(args)
        if length not in { 0, 1, }:
            raise TypeError(f"Need: at least 0 argument, at most 1 argument. Got: {length} arguments")

        if length == 1:
            chars = args[0]
            if chars is not None and not isinstance(chars, str):
                raise TypeError(f"Need: `None` or `str`. Got: `{str(chars)}` type=`{type(chars)}`")

        name = 'lstrip'
        func = self._MAPPING[name]

        operation = ( name, func, args, {}, )
        self._operations.append(operation)

        return self

    def max_length(self, length: int) -> Self:
        """
        Return value if type is `str` and length of the string less than `length`. Else - `None`.

        :param length: length of the string.
        """

        if not isinstance(length, int):
            raise TypeError(f"Need: `int`. Got: `{str(length)}` type=`{type(length)}`")

        if length < 1:
            raise ValueError(f"Need: value greater than 0. Got: `{length}`")

        name = 'max_length'
        func = self._MAPPING[name]

        operation = ( name, func, ( length, ), {}, )
        self._operations.append(operation)

        return self

    def min_length(self, length: int) -> Self:
        """
        Return value if type is `str` and length of the string more than `length`. Else - `None`.

        :param length: length of the string.
        """

        if not isinstance(length, int):
            raise TypeError(f"Need: `int`. Got: `{str(length)}` type=`{type(length)}`")

        if length < 1:
            raise ValueError(f"Need: value greater than 0. Got: `{str(length)}`")

        name = 'min_length'
        func = self._MAPPING[name]

        operation = ( name, func, ( length, ), {}, )
        self._operations.append(operation)

        return self

    def not_empty_str(self) -> Self:
        """
        Return value if type is `str` and length of the string more than `0`. Else - `None`.
        """

        name = 'not_empty_str'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self

    def removeprefix(self, prefix: str) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.removeprefix

        If type of value is `str` - modify and return. Else - `None`.
        """

        if not isinstance(prefix, str):
            raise TypeError(f"Need: `str`. Got: `{str(prefix)}` type=`{type(prefix)}`")

        name = 'removeprefix'
        func = self._MAPPING[name]

        operation = ( name, func, ( prefix, ), {}, )
        self._operations.append(operation)

        return self

    def removesuffix(self, prefix: str) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.removesuffix

        If type of value is `str` - modify and return. Else - `None`.
        """

        if not isinstance(prefix, str):
            raise TypeError(f"Need: `str`. Got: `{str(prefix)}` type=`{type(prefix)}`")

        name = 'removesuffix'
        func = self._MAPPING[name]

        operation = ( name, func, ( prefix, ), {}, )
        self._operations.append(operation)

        return self

    def replace(self,  *args) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.replace

        If type of value is `str` - modify and return. Else - `None`.
        """

        length = len(args)
        if length == 2:
            old, new, counter = args[0], args[1], None
        elif length == 3:
            old, new, counter = args[0], args[1], args[2]
        else:
            raise TypeError(f"Need: at least 2 arguments, at most 3 arguments, got `{length}`")

        if not isinstance(old, str):
            raise TypeError("replace() argument 1 must be `str`, not `int`")

        if not isinstance(new, str):
            raise TypeError("replace() argument 2 must be `str`, not `int`")

        if counter is not None and not isinstance(counter, int):
            raise TypeError("replace() argument 3 must be `int`")

        name = 'replace'
        func = self._MAPPING[name]
        args = ( old, new, ) if counter is None else ( old, new, counter, )

        operation = ( name, func, args, {}, )
        self._operations.append(operation)

        return self

    def re_sub(
        self,
        pattern: str | Pattern[str],
        repl: str | Callable[[Match[str]], str],
        string: str,
        count: int = 0,
        flags: int | RegexFlag = 0
    ) -> Self:
        """
        https://docs.python.org/3/library/re.html#re.sub

        If type of value is `str` - modify and return. Else - `None`.
        """

        name = 're_sub'
        func = self._MAPPING[name]
        args = ( pattern, repl, string, )
        kwargs = { 'count': count, 'flags': flags, }

        operation = ( name, func, args, kwargs, )
        self._operations.append(operation)

        return self

    def rstrip(self, *args) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.rstrip

        If type of value is `str` - modify and return. Else - `None`.
        """

        length = len(args)
        if length not in { 0, 1, }:
            raise TypeError(f"Need: at least 0 argument, at most 1 argument. Got: {length} arguments")

        if length == 1:
            chars = args[0]
            if chars is not None and not isinstance(chars, str):
                raise TypeError(f"Need: `None` or `str`. Got: `{str(chars)}` type=`{type(chars)}`")

        name = 'rstrip'
        func = self._MAPPING[name]

        operation = ( name, func, args, {}, )
        self._operations.append(operation)

        return self

    def startswith(self, *args) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.startswith

        If type of value is `str` and passes the check successfully. Else - `None`.
        """

        length = len(args)
        if length == 1:
            prefix, start, end = args[0], None, None
        elif length == 2:
            prefix, start, end = args[0], args[1], None
        elif length == 3:
            prefix, start, end = args[0], args[1], args[2]
        else:
            raise TypeError(f"Need: at least 0 argument, at most 3 argument. Got: {length} arguments")

        if isinstance(prefix, tuple):
            for _prefix in prefix:
                if not isinstance(_prefix, str):
                    raise TypeError(f"Need: `str`. Got: `{str(_prefix)}` type=`{type(_prefix)}`")
        elif not isinstance(prefix, ( str, tuple, )):
            raise TypeError(f"Need: `str` or `tuple[str]`. Got: `{str(prefix)}` type=`{type(prefix)}`")

        if start is not None and not isinstance(start, int):
            raise TypeError(f"Need: `int`. Got: `{str(start)}` type=`{type(start)}`")

        if end is not None and not isinstance(end, int):
            raise TypeError(f"Need: `int`. Got: `{str(end)}` type=`{type(end)}`")

        name = 'startswith'
        func = self._MAPPING[name]
        args = tuple( i for i in ( prefix, start, end, ) if i is not None )

        operation = ( name, func, args, {}, )
        self._operations.append(operation)

        return self

    def strip(self, *args) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.strip

        If type of value is `str` - modify and return. Else - `None`.
        """

        length = len(args)
        if length not in { 0, 1, }:
            raise TypeError(f"Need: at least 0 argument, at most 1 argument. Got: {length} arguments")

        if length == 1:
            chars = args[0]
            if chars is not None and not isinstance(chars, str):
                raise TypeError(f"Need: `None` or `str`. Got: `{str(chars)}` type=`{type(chars)}`")

        name = 'strip'
        func = self._MAPPING[name]

        operation = ( name, func, args, {}, )
        self._operations.append(operation)

        return self

    def upper(self) -> Self:
        """
        https://docs.python.org/3/library/stdtypes.html#str.upper

        If type of value is `str` - modify and return. Else - `None`.
        """

        name = 'upper'
        func = self._MAPPING[name]

        operation = ( name, func, tuple(), {}, )
        self._operations.append(operation)

        return self
