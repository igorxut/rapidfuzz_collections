
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
    RapidFuzzTuple
)

from data import data_tuple


# noinspection DuplicatedCode
class TestRapidFuzzTuple(TestCase):

    def test__init__(self):
        seq = ( 'test1', 'test2', )
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)

        rapidfuzz_tuple = RapidFuzzTuple(
            seq,
            normalizer=normalizer,
            score_cutoff=2,
            score_hint=1,
            scorer=Levenshtein.distance,  # noqa
            scorer_kwargs={ 'weights': ( 1, 2, 1, ), },
            scorer_type=ScorerType.DISTANCE,
            strategy=Strategy.BEST_ONLY_ONE
        )

        self.assertIsInstance(rapidfuzz_tuple, RapidFuzzTuple)

    def test__add__(self):
        rapidfuzz_tuple1 = RapidFuzzTuple(( 'test1', 'test2', 1, ))

        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, None)
        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, 'test1')
        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, 1)
        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, 1.1)
        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, { 1, 2, })
        self.assertRaises(TypeError, operator.add, rapidfuzz_tuple1, { 'k1': 'k2', })

        rapidfuzz_tuple2 = rapidfuzz_tuple1 + ( 'test3', 'test4', 2, )
        self.assertTupleEqual(tuple(rapidfuzz_tuple2), ( 'test1', 'test2', 1, 'test3', 'test4', 2, ))
        self.assertTupleEqual(rapidfuzz_tuple2.choices, ( 'test1', 'test2', None, 'test3', 'test4', None, ))

        rapidfuzz_tuple3 = rapidfuzz_tuple1 + RapidFuzzTuple(( 'test3', 'test4', 2, ))
        self.assertTupleEqual(tuple(rapidfuzz_tuple3), ( 'test1', 'test2', 1, 'test3', 'test4', 2, ))
        self.assertTupleEqual(rapidfuzz_tuple3.choices, ( 'test1', 'test2', None, 'test3', 'test4', None, ))

    def test__contains__(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', 1, ))

        self.assertTrue('test2' in rapidfuzz_tuple)
        self.assertFalse('test3' in rapidfuzz_tuple)

    def test__copy__(self):
        rapidfuzz_tuple1 = RapidFuzzTuple(( 'test1', [ 'test2', 1, ], ))
        rapidfuzz_tuple2 = copy(rapidfuzz_tuple1)

        self.assertTupleEqual(rapidfuzz_tuple1._data, rapidfuzz_tuple2._data)
        self.assertIs(rapidfuzz_tuple1._data, rapidfuzz_tuple2._data)
        self.assertIs(rapidfuzz_tuple1[1], rapidfuzz_tuple2[1])

    def test__deepcopy__(self):
        rapidfuzz_tuple1 = RapidFuzzTuple(( 'test1', [ 'test2', 1, ], ))
        rapidfuzz_tuple2 = deepcopy(rapidfuzz_tuple1)

        self.assertTupleEqual(rapidfuzz_tuple1._data, rapidfuzz_tuple2._data)
        self.assertIsNot(rapidfuzz_tuple1._data, rapidfuzz_tuple2._data)
        self.assertIsNot(rapidfuzz_tuple1[1], rapidfuzz_tuple2[1])

    def test__eq__(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', ))

        self.assertFalse(rapidfuzz_tuple == RapidFuzzTuple(( 'test3', 'test4', )))
        self.assertTrue(rapidfuzz_tuple == RapidFuzzTuple(( 'test1', 'test2', )))
        self.assertFalse(rapidfuzz_tuple == ( 'test5', 'test6', ))
        self.assertFalse(rapidfuzz_tuple == ( 'test1', 'test2', ))

    def test__getitem__(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', ))

        self.assertEqual(rapidfuzz_tuple[0], 'test1')
        self.assertEqual(rapidfuzz_tuple[1], 'test2')
        self.assertEqual(rapidfuzz_tuple[-1], 'test2')
        self.assertRaises(IndexError, lambda: rapidfuzz_tuple[2])

    def test__iter__(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', ))

        seq = tuple(i for i in rapidfuzz_tuple)

        self.assertTupleEqual(seq, ( 'test1', 'test2', ))

    def test__len__(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', 1, ))

        self.assertEqual(len(rapidfuzz_tuple), 3)

    def test__mul__(self):
        rapidfuzz_tuple1 = RapidFuzzTuple(( 'test1', 'test2', 1, ))

        self.assertRaises(TypeError, operator.mul, rapidfuzz_tuple1, None)
        self.assertRaises(TypeError, operator.mul, rapidfuzz_tuple1, 1.1)
        self.assertRaises(TypeError, operator.mul, rapidfuzz_tuple1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.mul, rapidfuzz_tuple1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.mul, rapidfuzz_tuple1, { 1, 2, })
        self.assertRaises(TypeError, operator.mul, rapidfuzz_tuple1, { 'k1': 'k2', })

        rapidfuzz_tuple2 = rapidfuzz_tuple1 * 2

        self.assertTupleEqual(tuple(rapidfuzz_tuple2), ( 'test1', 'test2', 1, 'test1', 'test2', 1, ))
        self.assertTupleEqual(rapidfuzz_tuple2.choices, ( 'test1', 'test2', None, 'test1', 'test2', None, ))

    def test__ne__(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', ))

        self.assertTrue(rapidfuzz_tuple != RapidFuzzTuple(( 'test3', 'test4', )))
        self.assertFalse(rapidfuzz_tuple != RapidFuzzTuple(( 'test1', 'test2', )))
        self.assertTrue(rapidfuzz_tuple != [ 'test5', 'test6', ])
        self.assertTrue(rapidfuzz_tuple != [ 'test1', 'test2', ])

    def test__repr__(self):
        rapidfuzz_tuple = RapidFuzzTuple([ 'test1', 'test2', ])

        self.assertEqual(repr(rapidfuzz_tuple), "RapidFuzzTuple(('test1', 'test2'))")

    def test__rmul__(self):
        rapidfuzz_tuple1 = RapidFuzzTuple(( 'test1', 'test2', 1, ))

        self.assertRaises(TypeError, operator.mul, None, rapidfuzz_tuple1)
        self.assertRaises(TypeError, operator.mul, 'test1', rapidfuzz_tuple1)
        self.assertRaises(TypeError, operator.mul, 1.1, rapidfuzz_tuple1)
        self.assertRaises(TypeError, operator.mul, [ 1, 2, ], rapidfuzz_tuple1)
        self.assertRaises(TypeError, operator.mul, ( 1, 2, ), rapidfuzz_tuple1)
        self.assertRaises(TypeError, operator.mul, { 1, 2, }, rapidfuzz_tuple1)
        self.assertRaises(TypeError, operator.mul, { 'k1': 'k2', }, rapidfuzz_tuple1)

        rapidfuzz_tuple2 = 2 * rapidfuzz_tuple1

        self.assertTupleEqual(tuple(rapidfuzz_tuple2), ( 'test1', 'test2', 1, 'test1', 'test2', 1, ))
        self.assertTupleEqual(rapidfuzz_tuple2.choices, ( 'test1', 'test2', None, 'test1', 'test2', None, ))

    def test_choices(self):
        rapidfuzz_tuple = RapidFuzzTuple(( '  tEst1', 'teSt2  ', 't3', '  t4  ', 1, 1.1, None, [ 1, 2, ], { 1, 2, }, ( 1, 2, ), { 'k1': 'k2', }, ))  # noqa: E501

        self.assertTupleEqual(rapidfuzz_tuple.choices, ( 'tEst1', 'teSt2', None, None, None, None, None, None, None, None, None, ))  # noqa: E501

    def test_count(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test2', 1, 'test1', ))

        self.assertEqual(rapidfuzz_tuple.count('test1'), 2)
        self.assertEqual(rapidfuzz_tuple.count('test2'), 1)
        self.assertEqual(rapidfuzz_tuple.count('test3'), 0)

    def test_index(self):
        rapidfuzz_tuple = RapidFuzzTuple(( 'test1', 'test1', 'test2', 1, 'test1', ))

        self.assertRaises(ValueError, lambda: rapidfuzz_tuple.index('test3'))

        self.assertEqual(rapidfuzz_tuple.index('test1'), 0)
        self.assertEqual(rapidfuzz_tuple.index('test2'), 2)
        self.assertEqual(rapidfuzz_tuple.index('test1', 1), 1)
        self.assertEqual(rapidfuzz_tuple.index('test1', 1, 4), 1)

    def test_fuzzy_contains(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_tuple = RapidFuzzTuple(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertTrue(rapidfuzz_tuple.fuzzy_contains('Australia', score_cutoff=100))

        # exact normalized key contains
        self.assertTrue(rapidfuzz_tuple.fuzzy_contains('   aUstraLia  ', score_cutoff=100))

        # similar key contains
        self.assertTrue(rapidfuzz_tuple.fuzzy_contains('Austraia'))
        self.assertTrue(rapidfuzz_tuple.fuzzy_contains('Ustralia'))
        self.assertFalse(rapidfuzz_tuple.fuzzy_contains('Gondor'))
        self.assertTrue(rapidfuzz_tuple.fuzzy_contains('Gondor', score_cutoff=60))
        self.assertFalse(rapidfuzz_tuple.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3))  # noqa: E501
        self.assertTrue(rapidfuzz_tuple.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4))  # noqa: E501

    def test_fuzzy_count(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_tuple = RapidFuzzTuple(data_tuple, normalizer=normalizer, score_cutoff=90)

        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Australia'), 1)  # Australia
        self.assertEqual(rapidfuzz_tuple.fuzzy_count('   aUstraLia  '), 1)  # Australia
        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Austraia'), 2)  # Australia, Austria
        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Ustralia'), 1)  # Australia
        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Gondor'), 0)

        # Andorra, El Salvador, Norfolk Island, Northern Mariana Islands, Republic of North Macedonia, Togo
        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Gondor', score_cutoff=60), 6)

        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3), 0)  # noqa: E501

        # Andorra, Ecuador, Gabon, Honduras, India, Jordan, Monaco, Togo, Tonga, Uganda
        self.assertEqual(rapidfuzz_tuple.fuzzy_count('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4), 10)  # noqa: E501

    def test_fuzzy_get(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_tuple = RapidFuzzTuple(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Australia', score_cutoff=100), 'Australia')

        # exact normalized key contains
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('   aUstraLia  ', score_cutoff=100), 'Australia')

        # similar key contains
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Austraia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertIsNone(rapidfuzz_tuple.fuzzy_get('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Austraia', strategy=Strategy.FIRST), 'Australia')
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Ustralia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Ustralia', strategy=Strategy.BEST_ONLY_ONE), 'Australia')  # noqa: E501
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Ustralia', strategy=Strategy.FIRST), 'Australia')
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Austria', strategy=Strategy.FIRST_FROM_BEST), 'Austria')  # noqa: E501
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Austria', strategy=Strategy.BEST_ONLY_ONE), 'Austria')
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Austria', strategy=Strategy.FIRST), 'Austria')
        self.assertIsNone(rapidfuzz_tuple.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_tuple.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_tuple.fuzzy_get('Gondor', strategy=Strategy.FIRST))
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), 'Andorra')  # noqa: E501
        self.assertIsNone(rapidfuzz_tuple.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))
        self.assertEqual(rapidfuzz_tuple.fuzzy_get('Gondor', strategy=Strategy.FIRST, score_cutoff=60), 'Andorra')  # noqa: E501

    def test_fuzzy_index(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_tuple = RapidFuzzTuple(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Australia', score_cutoff=100), 14)

        # exact normalized key contains
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('   aUstraLia  ', score_cutoff=100), 14)

        # similar key contains
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Austraia', strategy=Strategy.FIRST_FROM_BEST), 14)
        self.assertIsNone(rapidfuzz_tuple.fuzzy_index('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Austraia', strategy=Strategy.FIRST), 14)
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Ustralia', strategy=Strategy.FIRST_FROM_BEST), 14)
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Ustralia', strategy=Strategy.BEST_ONLY_ONE), 14)
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Ustralia', strategy=Strategy.FIRST), 14)
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Austria', strategy=Strategy.FIRST_FROM_BEST), 15)
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Austria', strategy=Strategy.BEST_ONLY_ONE), 15)
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Austria', strategy=Strategy.FIRST), 15)
        self.assertIsNone(rapidfuzz_tuple.fuzzy_index('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_tuple.fuzzy_index('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_tuple.fuzzy_index('Gondor', strategy=Strategy.FIRST))
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), 5)  # noqa: E501
        self.assertIsNone(rapidfuzz_tuple.fuzzy_index('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))
        self.assertEqual(rapidfuzz_tuple.fuzzy_index('Gondor', strategy=Strategy.FIRST, score_cutoff=60), 5)  # noqa: E501

    def test_get_fuzzy_scores(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_tuple = RapidFuzzTuple(data_tuple, normalizer=normalizer, score_cutoff=90)

        def _check(item) -> bool:
            return item[1] is not None

        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('Australia', score_cutoff=100))), ( ( 'Australia', 100.0, 14 ), ))  # noqa: E501
        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('   aUstraLia  ', score_cutoff=100))), ( ( 'Australia', 100.0, 14 ), ))  # noqa: E501
        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('Austraia'))), ( ( 'Australia', 94.11764705882352, 14, ), ( 'Austria', 93.33333333333333, 15, ), ))  # noqa: E501
        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('Ustralia'))), ( ( 'Australia', 94.11764705882352, 14, ), ))  # noqa: E501
        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('Austria'))), ( ('Austria', 100.0, 15, ), ))  # noqa: E501
        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('Gondor'))), tuple())
        self.assertTupleEqual(tuple(filter(_check, rapidfuzz_tuple.get_fuzzy_scores('Gondor', score_cutoff=60))), ( ( 'Andorra', 61.53846153846154, 5, ), ( 'Republic of North Macedonia', 60.00000000000001, 143, ), ( 'Northern Mariana Islands', 60.00000000000001, 149, ), ( 'Norfolk Island', 60.00000000000001, 161, ), ( 'El Salvador', 60.00000000000001, 200, ), ( 'Togo', 60.00000000000001, 217, ), ))  # noqa: E501

    def test_get_fuzzy_score_iter(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_tuple = RapidFuzzTuple(data_tuple, normalizer=normalizer, score_cutoff=90)

        targets = { ( 'Australia', 100.0, 14, ), }
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('Australia', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 100.0, 14, ), }
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('   aUstraLia  ', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, 14, ), ( 'Austria', 93.33333333333333, 15, ), }
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('Austraia'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, 14, ), }
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('Ustralia'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Austria', 100.0, 15, ), }
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('Austria'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = set()
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('Gondor'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Andorra', 61.53846153846154, 5, ), ( 'El Salvador', 60.00000000000001, 200, ), ( 'Norfolk Island', 60.00000000000001, 161, ), ( 'Northern Mariana Islands', 60.00000000000001, 149, ), ( 'Republic of North Macedonia', 60.00000000000001, 143, ), ( 'Togo', 60.00000000000001, 217, ), }  # noqa: E501
        source = set()
        for choice, score, index in rapidfuzz_tuple.get_fuzzy_score_iter('Gondor', score_cutoff=60):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)
