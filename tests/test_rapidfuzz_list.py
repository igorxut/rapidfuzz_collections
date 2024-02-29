
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
    RapidFuzzList
)

from data import data_tuple


# noinspection DuplicatedCode
class TestRapidFuzzList(TestCase):

    def test__init__(self):
        seq = [ 'test1', 'test2', ]
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)

        rapidfuzz_list = RapidFuzzList(
            seq,
            normalizer=normalizer,
            score_cutoff=2,
            score_hint=1,
            scorer=Levenshtein.distance,  # noqa
            scorer_kwargs={ 'weights': ( 1, 2, 1, ) },
            scorer_type=ScorerType.DISTANCE,
            strategy=Strategy.BEST_ONLY_ONE
        )

        self.assertIsInstance(rapidfuzz_list, RapidFuzzList)

    def test__add__(self):
        rapidfuzz_list1 = RapidFuzzList([ 'test1', 'test2', 1, ])

        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, None)
        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, 'test1')
        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, 1)
        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, 1.1)
        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, { 1, 2, })
        self.assertRaises(TypeError, operator.add, rapidfuzz_list1, { 'k1': 'k2', })

        rapidfuzz_list2 = rapidfuzz_list1 + [ 'test3', 'test4', 2, ]
        self.assertListEqual(list(rapidfuzz_list2), [ 'test1', 'test2', 1, 'test3', 'test4', 2, ])
        self.assertTupleEqual(rapidfuzz_list2.choices, ( 'test1', 'test2', None, 'test3', 'test4', None, ))

        rapidfuzz_list3 = rapidfuzz_list1 + RapidFuzzList([ 'test3', 'test4', 2, ])
        self.assertListEqual(list(rapidfuzz_list3), [ 'test1', 'test2', 1, 'test3', 'test4', 2, ])
        self.assertTupleEqual(rapidfuzz_list3.choices, ( 'test1', 'test2', None, 'test3', 'test4', None, ))

    def test__contains__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', 1, ])

        self.assertTrue('test2' in rapidfuzz_list)
        self.assertFalse('test3' in rapidfuzz_list)

    def test__copy__(self):
        rapidfuzz_list1 = RapidFuzzList([ 'test1', [ 'test2', 1, ], ])
        rapidfuzz_list2 = copy(rapidfuzz_list1)

        self.assertListEqual(rapidfuzz_list1._data, rapidfuzz_list2._data)
        self.assertIsNot(rapidfuzz_list1._data, rapidfuzz_list2._data)
        self.assertIs(rapidfuzz_list1[1], rapidfuzz_list2[1])

    def test__deepcopy__(self):
        rapidfuzz_list1 = RapidFuzzList([ 'test1', [ 'test2', 1, ], ])
        rapidfuzz_list2 = deepcopy(rapidfuzz_list1)

        self.assertListEqual(rapidfuzz_list1._data, rapidfuzz_list2._data)
        self.assertIsNot(rapidfuzz_list1._data, rapidfuzz_list2._data)
        self.assertIsNot(rapidfuzz_list1[1], rapidfuzz_list2[1])

    def test__delitem__(self):
        rapidfuzz_list = RapidFuzzList([ '  tEst1', 'teSt2  ', 't3', '  t4  ', ])

        def _check():
            del rapidfuzz_list[4]
        self.assertRaises(IndexError, _check)

        del rapidfuzz_list[1]
        self.assertListEqual(list(rapidfuzz_list), [ '  tEst1', 't3', '  t4  ', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'tEst1', None, None, ))

    def test__eq__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', ])

        self.assertFalse(rapidfuzz_list == RapidFuzzList([ 'test3', 'test4', ]))
        self.assertTrue(rapidfuzz_list == RapidFuzzList([ 'test1', 'test2', ]))
        self.assertFalse(rapidfuzz_list == [ 'test5', 'test6', ])
        self.assertFalse(rapidfuzz_list == [ 'test1', 'test2', ])

    def test__getitem__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', ])

        self.assertEqual(rapidfuzz_list[0], 'test1')
        self.assertEqual(rapidfuzz_list[1], 'test2')
        self.assertEqual(rapidfuzz_list[-1], 'test2')
        self.assertRaises(IndexError, lambda: rapidfuzz_list[2])

    def test__iadd__(self):
        rapidfuzz_list = RapidFuzzList([ '  test1 ', '  test2  ', ])

        self.assertRaises(TypeError, operator.iadd, rapidfuzz_list, None)

        rapidfuzz_list += RapidFuzzList([ '   test3', ])
        self.assertListEqual(list(rapidfuzz_list), [ '  test1 ', '  test2  ', '   test3', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', 'test2', 'test3', ))

        rapidfuzz_list += [ 'test4', ]
        self.assertListEqual(list(rapidfuzz_list), [ '  test1 ', '  test2  ', '   test3', 'test4', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', 'test2', 'test3', 'test4', ))

    def test__imul__(self):
        rapidfuzz_list = RapidFuzzList([ '  test1 ', '  test2  ', ])

        rapidfuzz_list *= 2

        self.assertListEqual(list(rapidfuzz_list), [ '  test1 ', '  test2  ', '  test1 ', '  test2  ', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', 'test2', 'test1', 'test2', ))

    def test__iter__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', ])

        seq = [ i for i in rapidfuzz_list ]

        self.assertListEqual(seq, [ 'test1', 'test2', ])

    def test__len__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', 1, ])

        self.assertEqual(len(rapidfuzz_list), 3)

    def test__mul__(self):
        rapidfuzz_list1 = RapidFuzzList([ 'test1', 'test2', 1, ])

        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, None)
        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, 'test1')
        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, 1.1)
        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, { 1, 2, })
        self.assertRaises(TypeError, operator.mul, rapidfuzz_list1, { 'k1': 'k2', })

        rapidfuzz_list2 = rapidfuzz_list1 * 2

        self.assertListEqual(list(rapidfuzz_list2), [ 'test1', 'test2', 1, 'test1', 'test2', 1, ])
        self.assertTupleEqual(rapidfuzz_list2.choices, ( 'test1', 'test2', None, 'test1', 'test2', None, ))

    def test__ne__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', ])

        self.assertTrue(rapidfuzz_list != RapidFuzzList([ 'test3', 'test4', ]))
        self.assertFalse(rapidfuzz_list != RapidFuzzList([ 'test1', 'test2', ]))
        self.assertTrue(rapidfuzz_list != [ 'test5', 'test6', ])
        self.assertTrue(rapidfuzz_list != [ 'test1', 'test2', ])

    def test__repr__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', ])

        self.assertEqual(repr(rapidfuzz_list), "RapidFuzzList(['test1', 'test2'])")

    def test__reversed__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', ])

        seq = [ i for i in reversed(rapidfuzz_list) ]

        self.assertListEqual(seq, [ 'test2', 'test1', ])

    def test__rmul__(self):
        rapidfuzz_list1 = RapidFuzzList([ 'test1', 'test2', 1, ])

        self.assertRaises(TypeError, operator.mul, None, rapidfuzz_list1)
        self.assertRaises(TypeError, operator.mul, 'test1', rapidfuzz_list1)
        self.assertRaises(TypeError, operator.mul, 1.1, rapidfuzz_list1)
        self.assertRaises(TypeError, operator.mul, [ 1, 2, ], rapidfuzz_list1)
        self.assertRaises(TypeError, operator.mul, ( 1, 2, ), rapidfuzz_list1)
        self.assertRaises(TypeError, operator.mul, { 1, 2, }, rapidfuzz_list1)
        self.assertRaises(TypeError, operator.mul, { 'k1': 'k2', }, rapidfuzz_list1)

        rapidfuzz_list2 = 2 * rapidfuzz_list1

        self.assertListEqual(list(rapidfuzz_list2), [ 'test1', 'test2', 1, 'test1', 'test2', 1, ])
        self.assertTupleEqual(rapidfuzz_list2.choices, ( 'test1', 'test2', None, 'test1', 'test2', None, ))

    def test__setitem__(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', 1, ])

        self.assertListEqual(list(rapidfuzz_list), [ 'test1', 'test2', 1, ])

        def _check():
            rapidfuzz_list[3] = 'test3'

        self.assertRaises(IndexError, _check)

        rapidfuzz_list[1] = 'test3'
        self.assertListEqual(list(rapidfuzz_list), [ 'test1', 'test3', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', 'test3', None, ))

        rapidfuzz_list[0] = 2
        self.assertListEqual(list(rapidfuzz_list), [ 2, 'test3', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, 'test3', None, ))

    def test_choices(self):
        rapidfuzz_list = RapidFuzzList([ '  tEst1', 'teSt2  ', 't3', '  t4  ', 1, 1.1, None, [ 1, 2, ], { 1, 2, }, ( 1, 2, ), { 'k1': 'k2', }, ])  # noqa: E501

        self.assertTupleEqual(rapidfuzz_list.choices, ( 'tEst1', 'teSt2', None, None, None, None, None, None, None, None, None, ))  # noqa: E501

    def test_append(self):
        rapidfuzz_list = RapidFuzzList()

        rapidfuzz_list.append(1)
        self.assertListEqual(list(rapidfuzz_list), [ 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, ))

        rapidfuzz_list.append(1.1)
        self.assertListEqual(list(rapidfuzz_list), [ 1, 1.1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, None, ))

        rapidfuzz_list.append(None)
        self.assertListEqual(list(rapidfuzz_list), [ 1, 1.1, None, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, None, None, ))

        rapidfuzz_list.append('  teSt  ')
        self.assertListEqual(list(rapidfuzz_list), [ 1, 1.1, None, '  teSt  ', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, None, None, 'teSt', ))

        rapidfuzz_list.append('t')
        self.assertListEqual(list(rapidfuzz_list), [ 1, 1.1, None, '  teSt  ', 't', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, None, None, 'teSt', None, ))

    def test_clear(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', 1, ])

        rapidfuzz_list.clear()

        self.assertListEqual(list(rapidfuzz_list), [])
        self.assertTupleEqual(rapidfuzz_list.choices, tuple())

    def test_copy(self):
        rapidfuzz_list1 = RapidFuzzList([ 'test1', [ 'test2', 1, ], ])
        rapidfuzz_list2 = rapidfuzz_list1.copy()

        self.assertListEqual(rapidfuzz_list1._data, rapidfuzz_list2._data)
        self.assertIsNot(rapidfuzz_list1._data, rapidfuzz_list2._data)
        self.assertIs(rapidfuzz_list1[1], rapidfuzz_list2[1])

    def test_count(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test2', 1, 'test1', ])

        self.assertEqual(rapidfuzz_list.count('test1'), 2)
        self.assertEqual(rapidfuzz_list.count('test2'), 1)
        self.assertEqual(rapidfuzz_list.count('test3'), 0)

    def test_extend(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', ])

        rapidfuzz_list.extend([ 1, 1.1, None, '  teSt2  ', 't', ])

        self.assertListEqual(list(rapidfuzz_list), [ 'test1', 1, 1.1, None, '  teSt2  ', 't', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', None, None, None, 'teSt2', None, ))

    def test_index(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 'test1', 'test2', 1, 'test1', ])

        self.assertRaises(ValueError, lambda: rapidfuzz_list.index('test3'))

        self.assertEqual(rapidfuzz_list.index('test1'), 0)
        self.assertEqual(rapidfuzz_list.index('test2'), 2)
        self.assertEqual(rapidfuzz_list.index('test1', 1), 1)
        self.assertEqual(rapidfuzz_list.index('test1', 1, 4), 1)

    def test_insert(self):
        rapidfuzz_list = RapidFuzzList([ '  test1 ', ' tEst2', 1, ])

        rapidfuzz_list.insert(0, 'test3')
        self.assertListEqual(list(rapidfuzz_list), [ 'test3', '  test1 ', ' tEst2', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test3', 'test1', 'tEst2', None, ))

        rapidfuzz_list.insert(1, 123)
        self.assertListEqual(list(rapidfuzz_list), [ 'test3', 123, '  test1 ', ' tEst2', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test3', None, 'test1', 'tEst2', None, ))

        rapidfuzz_list.insert(10, None)
        self.assertListEqual(list(rapidfuzz_list), [ 'test3', 123, '  test1 ', ' tEst2', 1, None, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test3', None, 'test1', 'tEst2', None, None, ))

        rapidfuzz_list.insert(-1, 7)
        self.assertListEqual(list(rapidfuzz_list), [ 'test3', 123, '  test1 ', ' tEst2', 1, 7, None, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test3', None, 'test1', 'tEst2', None, None, None, ))

    def test_pop(self):
        rapidfuzz_list = RapidFuzzList([ '  test1 ', ' tEst2', 1, ])

        item = rapidfuzz_list.pop(1)
        self.assertEqual(item, ' tEst2')
        self.assertListEqual(list(rapidfuzz_list), [ '  test1 ', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', None, ))

        self.assertRaises(IndexError, lambda: rapidfuzz_list.pop(2))

        item = rapidfuzz_list.pop()
        self.assertEqual(item, 1)
        self.assertListEqual(list(rapidfuzz_list), [ '  test1 ', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'test1', ))

        item = rapidfuzz_list.pop()
        self.assertEqual(item, '  test1 ')
        self.assertListEqual(list(rapidfuzz_list), [])
        self.assertTupleEqual(rapidfuzz_list.choices, tuple())

        self.assertRaises(IndexError, lambda: rapidfuzz_list.pop())

    def test_remove(self):
        rapidfuzz_list = RapidFuzzList([ 'teSt1', '  tEst2 ', 'teSt1', 1, ])

        rapidfuzz_list.remove('teSt1')
        self.assertListEqual(list(rapidfuzz_list), [ '  tEst2 ', 'teSt1', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'tEst2', 'teSt1', None, ))

        rapidfuzz_list.remove('teSt1')
        self.assertListEqual(list(rapidfuzz_list), [ '  tEst2 ', 1, ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'tEst2', None, ))

        self.assertRaises(ValueError, lambda: rapidfuzz_list.remove('teSt1'))
        self.assertRaises(ValueError, lambda: rapidfuzz_list.remove('teSt3'))

    def test_reverse(self):
        rapidfuzz_list = RapidFuzzList([ 'test1', 1, 'test2', 2, ])

        rapidfuzz_list.reverse()

        self.assertListEqual(list(rapidfuzz_list), [ 2, 'test2', 1, 'test1', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, 'test2', None, 'test1', ))

    def test_sort(self):
        rapidfuzz_list = RapidFuzzList([ 'etest', 'atest', 'z', 'utt', 'otest', 'itest', ])
        rapidfuzz_list.sort()
        self.assertListEqual(list(rapidfuzz_list), [ 'atest', 'etest', 'itest', 'otest', 'utt', 'z', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'atest', 'etest', 'itest', 'otest', 'utt', None, ))

        rapidfuzz_list = RapidFuzzList([ 'etest', 'atest', 'z', 'utt', 'otest', 'itest', ])
        rapidfuzz_list.sort(reverse=True)
        self.assertListEqual(list(rapidfuzz_list), [ 'z', 'utt', 'otest', 'itest', 'etest', 'atest', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, 'utt', 'otest', 'itest', 'etest', 'atest', ))

        rapidfuzz_list = RapidFuzzList([ 'etest', 'atest', 'z', 'utt', 'otest', 'itest', ])
        rapidfuzz_list.sort(key=len)
        self.assertListEqual(list(rapidfuzz_list), [ 'z', 'utt', 'etest', 'atest', 'otest', 'itest', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( None, 'utt', 'etest', 'atest', 'otest', 'itest', ))

        rapidfuzz_list = RapidFuzzList([ 'etest', 'atest', 'z', 'utt', 'otest', 'itest', ])
        rapidfuzz_list.sort(key=len, reverse=True)
        self.assertListEqual(list(rapidfuzz_list), [ 'etest', 'atest', 'otest', 'itest', 'utt', 'z', ])
        self.assertTupleEqual(rapidfuzz_list.choices, ( 'etest', 'atest', 'otest', 'itest', 'utt', None, ))

    def test_fuzzy_contains(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_list = RapidFuzzList(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertTrue(rapidfuzz_list.fuzzy_contains('Australia', score_cutoff=100))

        # exact normalized key contains
        self.assertTrue(rapidfuzz_list.fuzzy_contains('   aUstraLia  ', score_cutoff=100))

        # similar key contains
        self.assertTrue(rapidfuzz_list.fuzzy_contains('Austraia'))
        self.assertTrue(rapidfuzz_list.fuzzy_contains('Ustralia'))
        self.assertFalse(rapidfuzz_list.fuzzy_contains('Gondor'))
        self.assertTrue(rapidfuzz_list.fuzzy_contains('Gondor', score_cutoff=60))
        self.assertFalse(rapidfuzz_list.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3))  # noqa: E501
        self.assertTrue(rapidfuzz_list.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4))  # noqa: E501

    def test_fuzzy_count(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_list = RapidFuzzList(data_tuple, normalizer=normalizer, score_cutoff=90)

        self.assertEqual(rapidfuzz_list.fuzzy_count('Australia'), 1)  # Australia
        self.assertEqual(rapidfuzz_list.fuzzy_count('   aUstraLia  '), 1)  # Australia
        self.assertEqual(rapidfuzz_list.fuzzy_count('Austraia'), 2)  # Australia, Austria
        self.assertEqual(rapidfuzz_list.fuzzy_count('Ustralia'), 1)  # Australia
        self.assertEqual(rapidfuzz_list.fuzzy_count('Gondor'), 0)

        # Andorra, El Salvador, Norfolk Island, Northern Mariana Islands, Republic of North Macedonia, Togo
        self.assertEqual(rapidfuzz_list.fuzzy_count('Gondor', score_cutoff=60), 6)

        self.assertEqual(rapidfuzz_list.fuzzy_count('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3), 0)  # noqa: E501

        # Andorra, Ecuador, Gabon, Honduras, India, Jordan, Monaco, Togo, Tonga, Uganda
        self.assertEqual(rapidfuzz_list.fuzzy_count('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4), 10)  # noqa: E501

    def test_fuzzy_get(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_list = RapidFuzzList(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertEqual(rapidfuzz_list.fuzzy_get('Australia', score_cutoff=100), 'Australia')

        # exact normalized key contains
        self.assertEqual(rapidfuzz_list.fuzzy_get('   aUstraLia  ', score_cutoff=100), 'Australia')

        # similar key contains
        self.assertEqual(rapidfuzz_list.fuzzy_get('Austraia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertIsNone(rapidfuzz_list.fuzzy_get('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertEqual(rapidfuzz_list.fuzzy_get('Austraia', strategy=Strategy.FIRST), 'Australia')
        self.assertEqual(rapidfuzz_list.fuzzy_get('Ustralia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertEqual(rapidfuzz_list.fuzzy_get('Ustralia', strategy=Strategy.BEST_ONLY_ONE), 'Australia')  # noqa: E501
        self.assertEqual(rapidfuzz_list.fuzzy_get('Ustralia', strategy=Strategy.FIRST), 'Australia')
        self.assertEqual(rapidfuzz_list.fuzzy_get('Austria', strategy=Strategy.FIRST_FROM_BEST), 'Austria')
        self.assertEqual(rapidfuzz_list.fuzzy_get('Austria', strategy=Strategy.BEST_ONLY_ONE), 'Austria')
        self.assertEqual(rapidfuzz_list.fuzzy_get('Austria', strategy=Strategy.FIRST), 'Austria')
        self.assertIsNone(rapidfuzz_list.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_list.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_list.fuzzy_get('Gondor', strategy=Strategy.FIRST))
        self.assertEqual(rapidfuzz_list.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), 'Andorra')  # noqa: E501
        self.assertIsNone(rapidfuzz_list.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))
        self.assertEqual(rapidfuzz_list.fuzzy_get('Gondor', strategy=Strategy.FIRST, score_cutoff=60), 'Andorra')  # noqa: E501

    def test_fuzzy_index(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_list = RapidFuzzList(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertEqual(rapidfuzz_list.fuzzy_index('Australia', score_cutoff=100), 14)

        # exact normalized key contains
        self.assertEqual(rapidfuzz_list.fuzzy_index('   aUstraLia  ', score_cutoff=100), 14)

        # similar key contains
        self.assertEqual(rapidfuzz_list.fuzzy_index('Austraia', strategy=Strategy.FIRST_FROM_BEST), 14)
        self.assertIsNone(rapidfuzz_list.fuzzy_index('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertEqual(rapidfuzz_list.fuzzy_index('Austraia', strategy=Strategy.FIRST), 14)
        self.assertEqual(rapidfuzz_list.fuzzy_index('Ustralia', strategy=Strategy.FIRST_FROM_BEST), 14)
        self.assertEqual(rapidfuzz_list.fuzzy_index('Ustralia', strategy=Strategy.BEST_ONLY_ONE), 14)
        self.assertEqual(rapidfuzz_list.fuzzy_index('Ustralia', strategy=Strategy.FIRST), 14)
        self.assertEqual(rapidfuzz_list.fuzzy_index('Austria', strategy=Strategy.FIRST_FROM_BEST), 15)
        self.assertEqual(rapidfuzz_list.fuzzy_index('Austria', strategy=Strategy.BEST_ONLY_ONE), 15)
        self.assertEqual(rapidfuzz_list.fuzzy_index('Austria', strategy=Strategy.FIRST), 15)
        self.assertIsNone(rapidfuzz_list.fuzzy_index('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_list.fuzzy_index('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_list.fuzzy_index('Gondor', strategy=Strategy.FIRST))
        self.assertEqual(rapidfuzz_list.fuzzy_index('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), 5)  # noqa: E501
        self.assertIsNone(rapidfuzz_list.fuzzy_index('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))
        self.assertEqual(rapidfuzz_list.fuzzy_index('Gondor', strategy=Strategy.FIRST, score_cutoff=60), 5)

    def test_get_fuzzy_scores(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_list = RapidFuzzList(data_tuple, normalizer=normalizer, score_cutoff=90)

        def _check(item) -> bool:
            return item[1] is not None

        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('Australia', score_cutoff=100))), [ ( 'Australia', 100.0, 14, ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('   aUstraLia  ', score_cutoff=100))), [ ( 'Australia', 100.0, 14, ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('Austraia'))), [ ( 'Australia', 94.11764705882352, 14, ), ( 'Austria', 93.33333333333333, 15, ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('Ustralia'))), [ ( 'Australia', 94.11764705882352, 14, ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('Austria'))), [ ( 'Austria', 100.0, 15, ), ])  # noqa: E501
        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('Gondor'))), [])
        self.assertListEqual(list(filter(_check, rapidfuzz_list.get_fuzzy_scores('Gondor', score_cutoff=60))), [ ( 'Andorra', 61.53846153846154, 5, ), ( 'Republic of North Macedonia', 60.00000000000001, 143, ), ( 'Northern Mariana Islands', 60.00000000000001, 149, ), ( 'Norfolk Island', 60.00000000000001, 161, ), ( 'El Salvador', 60.00000000000001, 200, ), ( 'Togo', 60.00000000000001, 217, ), ])  # noqa: E501

    def test_get_fuzzy_score_iter(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_list = RapidFuzzList(data_tuple, normalizer=normalizer, score_cutoff=90)

        targets = { ( 'Australia', 100.0, 14, ), }
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('Australia', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 100.0, 14, ), }
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('   aUstraLia  ', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, 14, ), ( 'Austria', 93.33333333333333, 15, ), }
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('Austraia'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, 14, ), }
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('Ustralia'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Austria', 100.0, 15, ), }
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('Austria'):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)

        targets = set()
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('Gondor'):
            if score is not None:
                source.add((choice, score, index))
        self.assertSetEqual(targets, source)

        targets = { ( 'Andorra', 61.53846153846154, 5, ), ( 'El Salvador', 60.00000000000001, 200, ), ( 'Norfolk Island', 60.00000000000001, 161, ), ( 'Northern Mariana Islands', 60.00000000000001, 149, ), ( 'Republic of North Macedonia', 60.00000000000001, 143, ), ( 'Togo', 60.00000000000001, 217, ), }  # noqa: E501
        source = set()
        for choice, score, index in rapidfuzz_list.get_fuzzy_score_iter('Gondor', score_cutoff=60):
            if score is not None:
                source.add(( choice, score, index, ))
        self.assertSetEqual(targets, source)
