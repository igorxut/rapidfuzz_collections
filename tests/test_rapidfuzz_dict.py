
import operator

from copy import (
    copy,
    deepcopy
)
from rapidfuzz.distance import Levenshtein
from unittest import TestCase

from rapidfuzz_collections import (
    Normalizer,
    ScorerType,
    Strategy,
    RapidFuzzDict
)

from data import data_dict


# noinspection DuplicatedCode
class TestRapidFuzzDict(TestCase):

    def test__init__(self):
        seq = { 'test1': 1, 'test2': 2, }
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)

        rapidfuzz_dict = RapidFuzzDict(
            seq,
            normalizer=normalizer,
            score_cutoff=2,
            score_hint=1,
            scorer=Levenshtein.distance,  # noqa
            scorer_kwargs={ 'weights': ( 1, 2, 1, ) },
            scorer_type=ScorerType.DISTANCE,
            strategy=Strategy.BEST_ONLY_ONE
        )

        self.assertIsInstance(rapidfuzz_dict, RapidFuzzDict)

    def test__contains__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertTrue('test2' in rapidfuzz_dict)
        self.assertFalse('test3' in rapidfuzz_dict)

    def test__copy__(self):
        rapidfuzz_dict1 = RapidFuzzDict({ 'test1': [ 1, 2, ], })
        rapidfuzz_dict2 = copy(rapidfuzz_dict1)

        self.assertDictEqual(rapidfuzz_dict1._data, rapidfuzz_dict2._data)
        self.assertIsNot(rapidfuzz_dict1._data, rapidfuzz_dict2._data)
        self.assertIs(rapidfuzz_dict1['test1'], rapidfuzz_dict2['test1'])

        k1, v1 = rapidfuzz_dict1.popitem()
        k2, v2 = rapidfuzz_dict2.popitem()

        self.assertIs(k1, k2)

    def test__deepcopy__(self):
        rapidfuzz_dict1 = RapidFuzzDict({ 'test1': [ 1, 2, ], })
        rapidfuzz_dict2 = deepcopy(rapidfuzz_dict1)

        self.assertDictEqual(rapidfuzz_dict1._data, rapidfuzz_dict2._data)
        self.assertIsNot(rapidfuzz_dict1._data, rapidfuzz_dict2._data)
        self.assertIsNot(rapidfuzz_dict1['test1'], rapidfuzz_dict2['test1'])

        k1, v1 = rapidfuzz_dict1.popitem()
        k2, v2 = rapidfuzz_dict2.popitem()

        self.assertIs(k1, k2)

    def test__delitem__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': [ 2, 3, ], 'test1  ': 11, })

        def _check():
            del rapidfuzz_dict['test3']
        self.assertRaises(KeyError, _check)

        del rapidfuzz_dict['test2']
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, 'test1  ': 11, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, })

    def test__eq__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertFalse(rapidfuzz_dict == RapidFuzzDict({ 'test2': 1, 'test1': 2, }))
        self.assertTrue(rapidfuzz_dict == RapidFuzzDict({ 'test2': 2, 'test1': 1, }))
        self.assertFalse(rapidfuzz_dict == { 'test2': 1, 'test1': 2, })
        self.assertFalse(rapidfuzz_dict == { 'test2': 2, 'test1': 1, })

    def test__getitem__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertEqual(rapidfuzz_dict['test1'], 1)
        self.assertRaises(KeyError, lambda: rapidfuzz_dict['test3'])

    def test__ior__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, 'test1  ': 4, })
        rapidfuzz_dict |= { 'test1': 10, 'test3': 3, }
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 10, 'test2': 2, 'test3': 3, 'test1  ': 4, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, 'test1  ': 4, })
        rapidfuzz_dict |= RapidFuzzDict({ 'test1': 10, 'test3': 3, })
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 10, 'test2': 2, 'test1  ': 4, 'test3': 3, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

    def test__iter__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        seq = [ i for i in rapidfuzz_dict ]

        self.assertListEqual(seq, [ 'test1', 'test2', ])

    def test__len__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertEqual(len(rapidfuzz_dict), 2)

    def test__ne__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertTrue(rapidfuzz_dict != RapidFuzzDict({ 'test2': 1, 'test1': 2, }))
        self.assertFalse(rapidfuzz_dict != RapidFuzzDict({ 'test2': 2, 'test1': 1, }))
        self.assertTrue(rapidfuzz_dict != { 'test2': 1, 'test1': 2, })
        self.assertTrue(rapidfuzz_dict != { 'test2': 2, 'test1': 1, })

    def test__or__(self):
        rapidfuzz_dict1 = RapidFuzzDict({ 'test1': 1, 'test2': 2, 'test1  ': 4, })

        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, None)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, 'test1')
        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, 1)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, 1.1)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.or_, rapidfuzz_dict1, { 'k1', 'k2', })

        rapidfuzz_dict2 = rapidfuzz_dict1 | { 'test1': 10, 'test3': 3, }
        self.assertDictEqual(dict(rapidfuzz_dict2), { 'test1': 10, 'test2': 2, 'test1  ': 4, 'test3': 3, })
        self.assertDictEqual(rapidfuzz_dict2.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_dict3 = rapidfuzz_dict1 | RapidFuzzDict({ 'test1': 10, 'test3': 3, })
        self.assertDictEqual(dict(rapidfuzz_dict3), { 'test1': 10, 'test2': 2, 'test1  ': 4, 'test3': 3, })
        self.assertDictEqual(rapidfuzz_dict3.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

    def test__repr__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertEqual(repr(rapidfuzz_dict), "RapidFuzzDict({'test1': 1, 'test2': 2})")

    def test__reversed__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        seq = [ i for i in reversed(rapidfuzz_dict) ]

        self.assertListEqual(seq, [ 'test2', 'test1', ])

    def test__ror__(self):
        rapidfuzz_dict1 = RapidFuzzDict({ 'test1': 1, 'test2': 2, 'test1  ': 4, })

        self.assertRaises(TypeError, operator.or_, None, rapidfuzz_dict1)
        self.assertRaises(TypeError, operator.or_, 'test1', rapidfuzz_dict1)
        self.assertRaises(TypeError, operator.or_, 1, rapidfuzz_dict1)
        self.assertRaises(TypeError, operator.or_, 1.1, rapidfuzz_dict1)
        self.assertRaises(TypeError, operator.or_, ( 1, 2, ), rapidfuzz_dict1)
        self.assertRaises(TypeError, operator.or_, [ 1, 2, ], rapidfuzz_dict1)
        self.assertRaises(TypeError, operator.or_, { 'k1', 'k2', }, rapidfuzz_dict1)

        rapidfuzz_dict2 = { 'test1': 10, 'test3': 3, } | rapidfuzz_dict1
        self.assertDictEqual(dict(rapidfuzz_dict2), { 'test1': 1, 'test2': 2, 'test3': 3, 'test1  ': 4, })
        self.assertDictEqual(rapidfuzz_dict2.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

    def test__setitem__(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        rapidfuzz_dict['test3'] = 3
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, 'test2': 2, 'test3': 3, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_dict['test1'] = 10
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 10, 'test2': 2, 'test3': 3, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', }, 'test2': { 'test2', }, 'test3': { 'test3', }, })  # noqa: E501

    def test_choices(self):
        rapidfuzz_dict = RapidFuzzDict({ 1: 1, 1.1: 1.1, 'test1': 'test1', 'test1  ': 'test11', ( 2, 'test2', ): ( 2, 'test2', ), None: None, })  # noqa: E501

        self.assertDictEqual(rapidfuzz_dict.choices, { None: { None, 1, ( 2, 'test2', ), 1.1, }, 'test1': { 'test1', 'test1  ', }, })  # noqa: E501

    def test_clear(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        rapidfuzz_dict.clear()

        self.assertDictEqual(dict(rapidfuzz_dict), {})
        self.assertDictEqual(rapidfuzz_dict.choices, {})

    def test_copy(self):
        rapidfuzz_dict1 = RapidFuzzDict({ 'test1': [ 1, 2, ], })
        rapidfuzz_dict2 = rapidfuzz_dict1.copy()

        self.assertDictEqual(rapidfuzz_dict1._data, rapidfuzz_dict2._data)
        self.assertIsNot(rapidfuzz_dict1._data, rapidfuzz_dict2._data)
        self.assertIs(rapidfuzz_dict1['test1'], rapidfuzz_dict2['test1'])

        k1, v1 = rapidfuzz_dict1.popitem()
        k2, v2 = rapidfuzz_dict2.popitem()

        self.assertIs(k1, k2)

    def test_fromkeys(self):
        rapidfuzz_dict = RapidFuzzDict.fromkeys([ 'test1', 'test2', 'test1  ', ], 1)
        self.assertIsInstance(rapidfuzz_dict, RapidFuzzDict)
        self.assertDictEqual(rapidfuzz_dict._data, { 'test1': 1, 'test2': 1, 'test1  ': 1, })

        rapidfuzz_dict = RapidFuzzDict.fromkeys([ 'test1', 'test2', 'test1  ', ], 'value')
        self.assertIsInstance(rapidfuzz_dict, RapidFuzzDict)
        self.assertDictEqual(rapidfuzz_dict._data, { 'test1': 'value', 'test2': 'value', 'test1  ': 'value', })

        rapidfuzz_dict = RapidFuzzDict.fromkeys([ 'test1', 'test2', 'test1  ', ])
        self.assertIsInstance(rapidfuzz_dict, RapidFuzzDict)
        self.assertDictEqual(rapidfuzz_dict._data, { 'test1': None, 'test2': None, 'test1  ': None, })

        test_list = [ 1, ]
        rapidfuzz_dict = RapidFuzzDict.fromkeys([ 'test1', 'test2', 'test1  ', ], test_list)
        self.assertIsInstance(rapidfuzz_dict, RapidFuzzDict)
        self.assertDictEqual(rapidfuzz_dict._data, { 'test1': [ 1, ], 'test2': [ 1, ], 'test1  ': [ 1, ], })

        test_list.append(2)
        self.assertDictEqual(rapidfuzz_dict._data, { 'test1': [ 1, 2, ], 'test2': [ 1, 2, ], 'test1  ': [ 1, 2, ], })

    def test_get(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })

        self.assertEqual(rapidfuzz_dict.get('test1'), 1)
        self.assertEqual(rapidfuzz_dict.get('test3'), None)
        self.assertEqual(rapidfuzz_dict.get('test3', 3), 3)

    def test_items(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })
        result_list = [ ( 'test1', 1, ), ( 'test2', 2, ), ]

        for source, target in zip(rapidfuzz_dict.items(), result_list):
            self.assertTupleEqual(source, target)

    def test_keys(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })
        result_list = [ 'test1', 'test2', ]

        for source, target in zip(rapidfuzz_dict.keys(), result_list):
            self.assertEqual(source, target)

    def test_pop(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, 'test1  ': 10, })

        item = rapidfuzz_dict.pop('test2')
        self.assertEqual(item, 2)
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1,  'test1  ': 10, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, })

        self.assertRaises(KeyError, lambda: rapidfuzz_dict.pop('test3'))

        item = rapidfuzz_dict.pop('test3', 3)
        self.assertEqual(item, 3)
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1,  'test1  ': 10, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, })

    def test_popitem(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test1  ': 10, 'test2': 2, })

        item = rapidfuzz_dict.popitem()
        self.assertTupleEqual(item, ( 'test2', 2, ))
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, 'test1  ': 10, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, })

        item = rapidfuzz_dict.popitem()
        self.assertTupleEqual(item, ( 'test1  ', 10, ))
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', }, })

        item = rapidfuzz_dict.popitem()
        self.assertTupleEqual(item, ( 'test1', 1, ))
        self.assertDictEqual(dict(rapidfuzz_dict), {})
        self.assertDictEqual(rapidfuzz_dict.choices, {})

        self.assertRaises(KeyError, lambda: rapidfuzz_dict.popitem())

    def test_setdefault(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test1  ': 10, 'test2': 2, })

        item = rapidfuzz_dict.setdefault('test1', 2)
        self.assertEqual(item, 1)
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, 'test1  ': 10, 'test2': 2, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, })

        item = rapidfuzz_dict.setdefault('  test2 ', 20)
        self.assertEqual(item, 20)
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, 'test1  ': 10, 'test2': 2, '  test2 ': 20, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', '  test2 ', }, })  # noqa: E501

    def test_update(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test1  ': 10, 'test2': 2, })

        rapidfuzz_dict.update({ 'test1  ': 100, '  test2 ': 20, })
        self.assertDictEqual(dict(rapidfuzz_dict), { 'test1': 1, 'test1  ': 100, 'test2': 2, '  test2 ': 20, })
        self.assertDictEqual(rapidfuzz_dict.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', '  test2 ', }, })  # noqa: E501

    def test_values(self):
        rapidfuzz_dict = RapidFuzzDict({ 'test1': 1, 'test2': 2, })
        result_list = [ 1, 2, ]

        for source, target in zip(rapidfuzz_dict.values(), result_list):
            self.assertEqual(source, target)

    def test_fuzzy_contains(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_dict = RapidFuzzDict(data_dict, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertTrue(rapidfuzz_dict.fuzzy_contains('Australia', score_cutoff=100))

        # exact normalized key contains
        self.assertTrue(rapidfuzz_dict.fuzzy_contains('   aUstraLia  ', score_cutoff=100))

        # similar key contains
        self.assertTrue(rapidfuzz_dict.fuzzy_contains('Austraia'))
        self.assertTrue(rapidfuzz_dict.fuzzy_contains('Ustralia'))
        self.assertFalse(rapidfuzz_dict.fuzzy_contains('Gondor'))
        self.assertTrue(rapidfuzz_dict.fuzzy_contains('Gondor', score_cutoff=60))
        self.assertFalse(rapidfuzz_dict.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3))  # noqa: E501
        self.assertTrue(rapidfuzz_dict.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4))  # noqa: E501

    def test_fuzzy_get(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_dict = RapidFuzzDict(data_dict, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Australia', score_cutoff=100), ( 'Australia', 'AUS', ))  # noqa: E501

        # exact normalized key contains
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('   aUstraLia  ', score_cutoff=100), ( 'Australia', 'AUS', ))  # noqa: E501

        # similar key contains
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Austraia', strategy=Strategy.FIRST_FROM_BEST), ( 'Australia', 'AUS', ))  # noqa: E501
        self.assertIsNone(rapidfuzz_dict.fuzzy_get('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Austraia', strategy=Strategy.FIRST), ( 'Australia', 'AUS', ))  # noqa: E501
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Ustralia', strategy=Strategy.FIRST_FROM_BEST), ( 'Australia', 'AUS', ))  # noqa: E501
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Ustralia', strategy=Strategy.BEST_ONLY_ONE), ( 'Australia', 'AUS', ))  # noqa: E501
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Ustralia', strategy=Strategy.FIRST), ( 'Australia', 'AUS', ))  # noqa: E501
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Austria', strategy=Strategy.FIRST_FROM_BEST), ( 'Austria', 'AUT', ))  # noqa: E501
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Austria', strategy=Strategy.BEST_ONLY_ONE), ( 'Austria', 'AUT', ))  # noqa: E501
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Austria', strategy=Strategy.FIRST), ( 'Austria', 'AUT', ))  # noqa: E501
        self.assertIsNone(rapidfuzz_dict.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_dict.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_dict.fuzzy_get('Gondor', strategy=Strategy.FIRST))
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), ( 'Andorra', 'AND', ))  # noqa: E501
        self.assertIsNone(rapidfuzz_dict.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))
        self.assertTupleEqual(rapidfuzz_dict.fuzzy_get('Gondor', strategy=Strategy.FIRST, score_cutoff=60), ( 'Andorra', 'AND', ))  # noqa: E501

    def test_get_fuzzy_scores(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_dict = RapidFuzzDict(data_dict, normalizer=normalizer, score_cutoff=90)

        def _check(item) -> bool:
            return item[1] is not None

        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('Australia', score_cutoff=100))), [ ( 'AUS', 100.0, 'Australia', ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('   aUstraLia  ', score_cutoff=100))), [ ( 'AUS', 100.0, 'Australia', ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('Austraia'))), [ ( 'AUS', 94.11764705882352, 'Australia', ), ( 'AUT', 93.33333333333333, 'Austria', ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('Ustralia'))), [ ( 'AUS', 94.11764705882352, 'Australia', ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('Austria'))), [ ( 'AUT', 100.0, 'Austria', ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('Gondor'))), [])
        self.assertListEqual(list(filter(_check, rapidfuzz_dict.get_fuzzy_scores('Gondor', score_cutoff=60))), [ ( 'AND', 61.53846153846154, 'Andorra', ), ( 'MKD', 60.00000000000001, 'Republic of North Macedonia', ), ( 'MNP', 60.00000000000001, 'Northern Mariana Islands', ), ( 'NFK', 60.00000000000001, 'Norfolk Island', ), ( 'SLV', 60.00000000000001, 'El Salvador', ), ( 'TGO', 60.00000000000001, 'Togo', ), ])  # noqa: E501

    def test_get_fuzzy_score_iter(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_dict = RapidFuzzDict(data_dict, normalizer=normalizer, score_cutoff=90)

        targets = { ( 'AUS', 100.0, 'Australia', ), }
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Australia', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'AUS', 100.0, 'Australia', ), }
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('   aUstraLia  ', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'AUS', 94.11764705882352, 'Australia', ), ( 'AUT', 93.33333333333333, 'Austria', ), }
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Austraia'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'AUS', 94.11764705882352, 'Australia', ), }
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Ustralia'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'AUT', 100.0, 'Austria', ), }
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Austria'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = set()
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Gondor'):
            if score is not None:
                source.add((choice, score, index))
        self.assertSetEqual(targets, source)

        targets = { ( 'AND', 61.53846153846154, 'Andorra', ), ( 'MKD', 60.00000000000001, 'Republic of North Macedonia', ), ( 'MNP', 60.00000000000001, 'Northern Mariana Islands', ), ( 'NFK', 60.00000000000001, 'Norfolk Island', ), ( 'SLV', 60.00000000000001, 'El Salvador', ), ( 'TGO', 60.00000000000001, 'Togo', ), }  # noqa: E501
        source = set()
        for choice, score, index in rapidfuzz_dict.get_fuzzy_score_iter('Gondor', score_cutoff=60):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)
