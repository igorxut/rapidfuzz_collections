
# RapidFuzzCollections

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/igorxut/rapidfuzz_collections/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/rapidfuzz_collections)](https://pypi.org/project/rapidfuzz_collections/)
[![Python versions](https://img.shields.io/pypi/pyversions/rapidfuzz_collections)](https://www.python.org)

## Description

A collection of datatypes, using rapidfuzz to allow for fuzzy-string matching:

- RapidFuzzList
- RapidFuzzTuple
- RapidFuzzSet
- RapidFuzzFrozenSet
- RapidFuzzDict

Default collection's classes extended by methods for fuzzy-string matching.  
The main idea is using additional memory for keep normalized values of collection.

## Requirements

- Python 3.12 or later
- [rapidfuzz](https://github.com/rapidfuzz/RapidFuzz/)

## Installation

Can be installed with `pip` the following way:

```bash
pip install rapidfuzz_collections
```

## License

RapidFuzzCollections is licensed under the MIT license.

## Usage

Example:

```python
from rapidfuzz_collections import (
    Normalizer,
    RapidFuzzDict
)


# key is country name, value is country code
data_dict = {
    'Aruba': "ABW",
    'Afghanistan': "AFG",
    'Australia': "AUS",
    'Austria': "AUT",
    # ...
}

normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
rapidfuzz_dict = RapidFuzzDict(data_dict, normalizer=normalizer, score_cutoff=90)

rapidfuzz_dict.fuzzy_contains('Gondor')  # False
rapidfuzz_dict.fuzzy_contains('Ustralia')  # True
rapidfuzz_dict.fuzzy_get('Ustralia')  # ( 'Australia', 'AUS', )
rapidfuzz_dict.get_fuzzy_scores('Austraia')  # [ ( 'AUS', 94.11764705882352, 'Australia', ), ( 'AUT', 93.33333333333333, 'Austria', ), ( 'ABW', None, 'Aruba', ), ( 'AFG', None, 'Afghanistan', ), ... ]

result = set()
for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Austraia'):
    if score is not None:
        result.add(( choice, score, index, ))
# result == { ( 'AUS', 94.11764705882352, 'Australia', ), ( 'AUT', 93.33333333333333, 'Austria', ), }
```
