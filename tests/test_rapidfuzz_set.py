
import operator

from copy import copy
from rapidfuzz.distance import Levenshtein
from unittest import TestCase

from rapidfuzz_collections import (
    Normalizer,
    ScorerType,
    Strategy,
    RapidFuzzSet
)

from data import data_tuple


# noinspection DuplicatedCode
class TestRapidFuzzSet(TestCase):

    def test__init__(self):
        seq = { 'test1', 'test2', }
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)

        rapidfuzz_set = RapidFuzzSet(
            seq,
            normalizer=normalizer,
            score_cutoff=2,
            score_hint=1,
            scorer=Levenshtein.distance,  # noqa
            scorer_kwargs={ 'weights': ( 1, 2, 1, ), },
            scorer_type=ScorerType.DISTANCE,
            strategy=Strategy.BEST_ONLY_ONE
        )

        self.assertIsInstance(rapidfuzz_set, RapidFuzzSet)

    def test__and__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, None)
        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, 'test1')
        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, 1)
        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, 1.1)
        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.and_, rapidfuzz_set1, { 'k1': 'k2', })

        rapidfuzz_set2 = rapidfuzz_set1 & RapidFuzzSet({ 'test3', 'test4', })
        self.assertSetEqual(set(rapidfuzz_set2), { 'test3', })

        rapidfuzz_set3 = rapidfuzz_set1 & { 'test3', 'test4', }
        self.assertSetEqual(set(rapidfuzz_set3), { 'test3', })

        rapidfuzz_set4 = rapidfuzz_set1 & frozenset({ 'test3', 'test4', })
        self.assertSetEqual(set(rapidfuzz_set4), { 'test3', })

    def test__contains__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, })

        self.assertTrue('test2' in rapidfuzz_set)
        self.assertFalse('test3' in rapidfuzz_set)

    def test__copy__(self):
        rapidfuzz_set1 = RapidFuzzSet({ ( 'test1', ), })
        rapidfuzz_set2 = copy(rapidfuzz_set1)

        self.assertSetEqual(rapidfuzz_set1._data, rapidfuzz_set2._data)
        self.assertIsNot(rapidfuzz_set1._data, rapidfuzz_set2._data)

        element1 = rapidfuzz_set1.pop()
        element2 = rapidfuzz_set2.pop()

        self.assertIs(element1, element2)

    def test__eq__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test1', })

        self.assertFalse(rapidfuzz_set == RapidFuzzSet({ 'test3', 'test4', }))
        self.assertTrue(rapidfuzz_set == RapidFuzzSet({ 'test1', 'test2', }))
        self.assertFalse(rapidfuzz_set == { 'test5', 'test6', })
        self.assertFalse(rapidfuzz_set == { 'test1', 'test2', })
        self.assertFalse(rapidfuzz_set == frozenset({ 'test5', 'test6', }))
        self.assertFalse(rapidfuzz_set == frozenset({ 'test1', 'test2', }))

    def test__iand__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })

        self.assertRaises(TypeError, operator.iand, rapidfuzz_set, None)

        rapidfuzz_set &= { 'test1', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', }, })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set &= RapidFuzzSet({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', }, })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', })
        rapidfuzz_set &= { 'test3', }
        self.assertSetEqual(set(rapidfuzz_set), set())
        self.assertDictEqual(rapidfuzz_set.choices, {})

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', })
        rapidfuzz_set &= frozenset({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), set())
        self.assertDictEqual(rapidfuzz_set.choices, {})

    def test__ior__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set |= { 'test1', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set |= frozenset({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set |= RapidFuzzSet({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set |= { 'test3', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', 'test3', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set |= frozenset({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', 'test3', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set |= RapidFuzzSet({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', 'test3', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, 'test3': { 'test3', }, })  # noqa: E501

    def test__isub__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set -= { 'test1', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set -= frozenset({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set -= RapidFuzzSet({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set -= { 'test3', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set -= frozenset({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set -= RapidFuzzSet({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

    def test__iter__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', })

        seq = { i for i in rapidfuzz_set }

        self.assertSetEqual(seq, { 'test1', 'test2', })

    def test__ixor__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set ^= { 'test1', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set ^= frozenset({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set ^= RapidFuzzSet({ 'test1', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', 1, '  test1  ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set ^= { 'test3', }
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', 'test3', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })
        rapidfuzz_set ^= frozenset({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', 'test3', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_set = RapidFuzzSet({'test1', 'test2', 1, 'test1', '  test1  '})
        rapidfuzz_set ^= RapidFuzzSet({ 'test3', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test2', 1, '  test1  ', 'test3', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1  ', }, 'test2': { 'test2', }, None: { 1, }, 'test3': { 'test3', }, })  # noqa: E501

    def test__len__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, })

        self.assertEqual(len(rapidfuzz_set), 3)

    def test__ne__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test1', })

        self.assertTrue(rapidfuzz_set != RapidFuzzSet({ 'test3', 'test4', }))
        self.assertFalse(rapidfuzz_set != RapidFuzzSet({ 'test1', 'test2', }))
        self.assertTrue(rapidfuzz_set != { 'test5', 'test6', })
        self.assertTrue(rapidfuzz_set != { 'test1', 'test2', })
        self.assertTrue(rapidfuzz_set != frozenset({ 'test5', 'test6', }))
        self.assertTrue(rapidfuzz_set != frozenset({ 'test1', 'test2', }))

    def test__or__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })

        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, None)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, 'test1')
        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, 1)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, 1.1)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.or_, rapidfuzz_set1, { 'k1': 'k2', })

        rapidfuzz_set2 = rapidfuzz_set1 | { 'test2', 'test4', 2, }
        self.assertSetEqual(set(rapidfuzz_set2), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_set2.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

        rapidfuzz_set3 = rapidfuzz_set1 | frozenset({ 'test2', 'test4', 2, })
        self.assertSetEqual(set(rapidfuzz_set3), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_set3.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

        rapidfuzz_set4 = rapidfuzz_set1 | RapidFuzzSet({ 'test3', 'test4', 2, })
        self.assertSetEqual(set(rapidfuzz_set4), { 1, 2, 'test2', 'test4', '  test1  ', 'test1', 'test3', })
        self.assertDictEqual(rapidfuzz_set4.choices, { None: { 1, 2, }, 'test2': { 'test2', }, 'test4': { 'test4', }, 'test1': { '  test1  ', 'test1', }, 'test3': {'test3'}, })  # noqa: E501

    def test__rand_(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, operator.and_, None, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.and_, 'test1', rapidfuzz_set1)
        self.assertRaises(TypeError, operator.and_, 1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.and_, 1.1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.and_, ( 1, 2, ), rapidfuzz_set1)
        self.assertRaises(TypeError, operator.and_, [ 1, 2, ], rapidfuzz_set1)
        self.assertRaises(TypeError, operator.and_, { 'k1': 'k2', }, rapidfuzz_set1)

        rapidfuzz_set2 = { 'test3', 'test4', } & rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set2), { 'test3', })

        rapidfuzz_set3 = frozenset({ 'test3', 'test4', }) & rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set3), { 'test3', })

    def test__repr__(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', })

        self.assertEqual(repr(rapidfuzz_set), "RapidFuzzSet({'test1'})")

    def test__ror__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })

        self.assertRaises(TypeError, operator.or_, None, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.or_, 'test1', rapidfuzz_set1)
        self.assertRaises(TypeError, operator.or_, 1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.or_, 1.1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.or_, ( 1, 2, ), rapidfuzz_set1)
        self.assertRaises(TypeError, operator.or_, [ 1, 2, ], rapidfuzz_set1)
        self.assertRaises(TypeError, operator.or_, { 'k1': 'k2', }, rapidfuzz_set1)

        rapidfuzz_set2 = { 'test2', 'test4', 2, } | rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set2), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_set2.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

        rapidfuzz_set3 = frozenset({ 'test2', 'test4', 2, }) | rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set3), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_set3.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

    def test__rsub__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.sub, None, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.sub, 'test1', rapidfuzz_set1)
        self.assertRaises(TypeError, operator.sub, 1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.sub, 1.1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.sub, [ 1, 2, ], rapidfuzz_set1)
        self.assertRaises(TypeError, operator.sub, ( 1, 2, ), rapidfuzz_set1)
        self.assertRaises(TypeError, operator.sub, { 'k1': 'k2', }, rapidfuzz_set1)

        rapidfuzz_set2 = { 'test3', 'test2', } - rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set2), { 'test3', })
        self.assertDictEqual(rapidfuzz_set2.choices, { 'test3': { 'test3', }, })

        rapidfuzz_set3 = frozenset({ 'test3', 'test2', }) - rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set3), { 'test3', })
        self.assertDictEqual(rapidfuzz_set3.choices, { 'test3': { 'test3', }, })

    def test__rxor__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.xor, None, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.xor, 'test1', rapidfuzz_set1)
        self.assertRaises(TypeError, operator.xor, 1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.xor, 1.1, rapidfuzz_set1)
        self.assertRaises(TypeError, operator.xor, [ 1, 2, ], rapidfuzz_set1)
        self.assertRaises(TypeError, operator.xor, ( 1, 2, ), rapidfuzz_set1)
        self.assertRaises(TypeError, operator.xor, { 'k1': 'k2', }, rapidfuzz_set1)

        rapidfuzz_set2 = { 'test3', 'test2', } ^ rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set2), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_set2.choices, { None: { 1, }, 'test3': { 'test3', }, 'test1': { 'test1', }, })  # noqa: E501

        rapidfuzz_set3 = frozenset({ 'test3', 'test2', }) ^ rapidfuzz_set1
        self.assertSetEqual(set(rapidfuzz_set3), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_set3.choices, { None: { 1, }, 'test3': { 'test3', }, 'test1': { 'test1', }, })  # noqa: E501

    def test__sub__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, None)
        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, 'test1')
        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, 1)
        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, 1.1)
        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.sub, rapidfuzz_set1, { 'k1': 'k2', })

        rapidfuzz_set2 = rapidfuzz_set1 - { 'test3', 'test2', }
        self.assertSetEqual(set(rapidfuzz_set2), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_set2.choices, { 'test1': { 'test1', }, None: { 1, }, })

        rapidfuzz_set3 = rapidfuzz_set1 - frozenset({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_set3), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_set3.choices, { 'test1': { 'test1', }, None: { 1, }, })

        rapidfuzz_set4 = rapidfuzz_set1 - RapidFuzzSet({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_set4), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_set4.choices, { 'test1': { 'test1', }, None: { 1, }, })

    def test__xor__(self):
        rapidfuzz_set1 = RapidFuzzSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, None)
        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, 'test1')
        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, 1)
        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, 1.1)
        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.xor, rapidfuzz_set1, { 'k1': 'k2', })

        rapidfuzz_set2 = rapidfuzz_set1 ^ { 'test3', 'test2', }
        self.assertSetEqual(set(rapidfuzz_set2), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_set2.choices, { None: { 1, }, 'test1': { 'test1', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_set3 = rapidfuzz_set1 ^ frozenset({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_set3), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_set3.choices, { None: { 1, }, 'test1': { 'test1', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_set4 = rapidfuzz_set1 ^ RapidFuzzSet({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_set4), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_set4.choices, { None: { 1, }, 'test1': { 'test1', }, 'test3': { 'test3', }, })  # noqa: E501

    def test_choices(self):
        rapidfuzz_set = RapidFuzzSet({ '  tEst1', 'teSt2  ', 't3', '  t4  ', 1, 1.1, None, })

        self.assertDictEqual(rapidfuzz_set.choices, { None: { None, 1, 1.1, '  t4  ', 't3'}, 'tEst1': { '  tEst1', }, 'teSt2': { 'teSt2  ', }, })  # noqa: E501

    def test_add(self):
        rapidfuzz_set = RapidFuzzSet()

        rapidfuzz_set.add('test1')
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', }, })

        rapidfuzz_set.add(1)
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_set.choices, { None: { 1, }, 'test1': { 'test1', }, })

        rapidfuzz_set.add(None)
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 1, None, })
        self.assertDictEqual(rapidfuzz_set.choices, { None: { 1, None, }, 'test1': { 'test1', }, })

        rapidfuzz_set.add('test1   ')
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 1, None, 'test1   ', })
        self.assertDictEqual(rapidfuzz_set.choices, { None: { 1, None, }, 'test1': { 'test1', 'test1   ', }, })

        rapidfuzz_set.add('test1')
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 1, None, 'test1   ', })
        self.assertDictEqual(rapidfuzz_set.choices, { None: { 1, None, }, 'test1': { 'test1', 'test1   ', }, })

    def test_clear(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 1, })

        rapidfuzz_set.clear()

        self.assertSetEqual(set(rapidfuzz_set), set())
        self.assertDictEqual(rapidfuzz_set.choices, {})

    def test_copy(self):
        rapidfuzz_set1 = RapidFuzzSet({ ( 'test1', ), })
        rapidfuzz_set2 = copy(rapidfuzz_set1)

        self.assertSetEqual(rapidfuzz_set1._data, rapidfuzz_set2._data)
        self.assertIsNot(rapidfuzz_set1._data, rapidfuzz_set2._data)

        element1 = rapidfuzz_set1.pop()
        element2 = rapidfuzz_set2.pop()

        self.assertIs(element1, element2)

    def test_difference(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_set.difference(RapidFuzzSet({ 'test1', 'test4', }))), { 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_set.difference({ 'test1', 'test4', })), { 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_set.difference({ 'test1', 'test4', }, { 'test2', 'test5', })), { 'test3', })  # noqa: E501

    def test_difference_update(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.difference_update({ 'k1': 'k2', }))

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.difference_update(RapidFuzzSet({ 'test1', 'test4', }))
        self.assertSetEqual(set(rapidfuzz_set), { 'test3', 'test2', })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.difference_update({ 'test1', 'test4', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test3', 'test2', })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.difference_update({ 'test1', 'test4', }, { 'test2', 'test5', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test3', })

    def test_discard(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', '  tEst2 ', '   test1', 1, })

        rapidfuzz_set.discard('teSt134')
        self.assertSetEqual(set(rapidfuzz_set), { '   test1', 1, 'test1', '  tEst2 ', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '   test1', 'test1', }, None: { 1, }, 'tEst2': { '  tEst2 ', }, })  # noqa: E501

        rapidfuzz_set.discard('   test1')
        self.assertSetEqual(set(rapidfuzz_set), { '  tEst2 ', 'test1', 1, })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', }, 'tEst2': { '  tEst2 ', }, None: { 1, }, })  # noqa: E501

    def test_intersection(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_set.intersection(RapidFuzzSet({ 'test1', 'test4', }))), { 'test1', })
        self.assertSetEqual(set(rapidfuzz_set.intersection({ 'test1', 'test4', })), { 'test1', })
        self.assertSetEqual(set(rapidfuzz_set.intersection({ 'test2', 'test4', }, { 'test2', 'test5', })), { 'test2', })  # noqa: E501

    def test_intersection_update(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.intersection_update({ 'k1': 'k2', }))

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.intersection_update(RapidFuzzSet({ 'test1', 'test4', }))
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.intersection_update({ 'test1', 'test4', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.intersection_update({ 'test2', 'test4', }, { 'test2', 'test5', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test2', })

    # noinspection PyTypeChecker
    def test_isdisjoint(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.isdisjoint({ 'k1': 'k2', }))

        self.assertTrue(rapidfuzz_set.isdisjoint(RapidFuzzSet({ 'test3', 'test4', })))
        self.assertTrue(rapidfuzz_set.isdisjoint({ 'test3', 'test4', }))
        self.assertFalse(rapidfuzz_set.isdisjoint(RapidFuzzSet({ 'test1', 'test4', })))
        self.assertFalse(rapidfuzz_set.isdisjoint({ 'test1', 'test4', }))

    # noinspection PyTypeChecker
    def test_issubset(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issubset({ 'k1': 'k2', }))

        self.assertTrue(rapidfuzz_set.issubset(RapidFuzzSet({ 'test1', 'test2', 'test3', })))
        self.assertTrue(rapidfuzz_set.issubset({ 'test1', 'test2', 'test3', }))
        self.assertFalse(rapidfuzz_set.issubset(RapidFuzzSet({ 'test11', 'test22', 'test3', })))
        self.assertFalse(rapidfuzz_set.issubset({ 'test11', 'test22', 'test3', }))

    # noinspection PyTypeChecker
    def issuperset(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.issuperset({ 'k1': 'k2', }))

        self.assertTrue(rapidfuzz_set.issuperset(RapidFuzzSet({ 'test2', 'test3', })))
        self.assertTrue(rapidfuzz_set.issuperset({ 'test2', 'test3', }))
        self.assertFalse(rapidfuzz_set.issuperset(RapidFuzzSet({ 'test1', 'test22', 'test3', })))
        self.assertFalse(rapidfuzz_set.issuperset({ 'test1', 'test22', 'test3', }))

    def test_pop(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', })

        item = rapidfuzz_set.pop()
        self.assertEqual(item, 'test1')
        self.assertSetEqual(set(rapidfuzz_set), set())
        self.assertDictEqual(rapidfuzz_set.choices, {})

        self.assertRaises(KeyError, lambda: rapidfuzz_set.pop())

    def test_remove(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', '  test1', 1, })

        rapidfuzz_set.remove('test2')
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', '  test1', 1, })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', '  test1', }, None: { 1, }, })

        rapidfuzz_set.remove('test1')
        self.assertSetEqual(set(rapidfuzz_set), { '  test1', 1, })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { '  test1', }, None: { 1, }, })

        self.assertRaises(KeyError, lambda: rapidfuzz_set.remove('test3'))

    # noinspection PyTypeChecker
    def test_symmetric_difference(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_set.symmetric_difference(RapidFuzzSet({ 'test1', 'test4', }))), { 'test4', 'test3', 'test2', })  # noqa: E501
        self.assertSetEqual(set(rapidfuzz_set.symmetric_difference({ 'test1', 'test4', })), { 'test4', 'test3', 'test2', })  # noqa: E501

    # noinspection PyTypeChecker
    def test_symmetric_difference_update(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.symmetric_difference_update({ 'k1': 'k2', }))

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.symmetric_difference_update(RapidFuzzSet({ 'test1', 'test4', }))
        self.assertSetEqual(set(rapidfuzz_set), { 'test4', 'test3', 'test2', })

        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test3', })
        rapidfuzz_set.symmetric_difference_update({ 'test1', 'test4', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test4', 'test3', 'test2', })

    def test_union(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.union(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.union('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.union(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.union(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.union([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.union(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.union({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_set.union(RapidFuzzSet({ 'test1', 'test3', }), { 'test2', 'test4', })), { 'test1', 'test2', 'test3', 'test4', })  # noqa: E501

    def test_update(self):
        rapidfuzz_set = RapidFuzzSet({ 'test1', 'test2', 'test1  ' })

        self.assertRaises(TypeError, lambda: rapidfuzz_set.update(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.update('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.update(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.update(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.update([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.update(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_set.update({ 'k1': 'k2', }))

        rapidfuzz_set.update(RapidFuzzSet({ 'test1', 'test3', }), { 'test2', 'test4', })
        self.assertSetEqual(set(rapidfuzz_set), { 'test1', 'test1  ', 'test2', 'test3', 'test4', })
        self.assertDictEqual(rapidfuzz_set.choices, { 'test1': { 'test1', 'test1  ', }, 'test2': { 'test2', }, 'test3': { 'test3', }, 'test4': { 'test4', }, })  # noqa: E501

    def test_fuzzy_contains(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_set = RapidFuzzSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertTrue(rapidfuzz_set.fuzzy_contains('Australia', score_cutoff=100))

        # exact normalized key contains
        self.assertTrue(rapidfuzz_set.fuzzy_contains('   aUstraLia  ', score_cutoff=100))

        # similar key contains
        self.assertTrue(rapidfuzz_set.fuzzy_contains('Austraia'))
        self.assertTrue(rapidfuzz_set.fuzzy_contains('Ustralia'))
        self.assertFalse(rapidfuzz_set.fuzzy_contains('Gondor'))
        self.assertTrue(rapidfuzz_set.fuzzy_contains('Gondor', score_cutoff=60))
        self.assertFalse(rapidfuzz_set.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3))  # noqa: E501
        self.assertTrue(rapidfuzz_set.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4))  # noqa: E501

    def test_fuzzy_get(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_set = RapidFuzzSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertEqual(rapidfuzz_set.fuzzy_get('Australia', score_cutoff=100), 'Australia')

        # exact normalized key contains
        self.assertEqual(rapidfuzz_set.fuzzy_get('   aUstraLia  ', score_cutoff=100), 'Australia')

        # similar key contains
        self.assertEqual(rapidfuzz_set.fuzzy_get('Austraia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertIsNone(rapidfuzz_set.fuzzy_get('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIn(rapidfuzz_set.fuzzy_get('Austraia', strategy=Strategy.FIRST), { 'Austria', 'Australia', })
        self.assertEqual(rapidfuzz_set.fuzzy_get('Ustralia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertEqual(rapidfuzz_set.fuzzy_get('Ustralia', strategy=Strategy.BEST_ONLY_ONE), 'Australia')
        self.assertEqual(rapidfuzz_set.fuzzy_get('Ustralia', strategy=Strategy.FIRST), 'Australia')
        self.assertEqual(rapidfuzz_set.fuzzy_get('Austria', strategy=Strategy.FIRST_FROM_BEST), 'Austria')
        self.assertEqual(rapidfuzz_set.fuzzy_get('Austria', strategy=Strategy.BEST_ONLY_ONE), 'Austria')
        self.assertEqual(rapidfuzz_set.fuzzy_get('Austria', strategy=Strategy.FIRST), 'Austria')
        self.assertIsNone(rapidfuzz_set.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_set.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_set.fuzzy_get('Gondor', strategy=Strategy.FIRST))
        self.assertEqual(rapidfuzz_set.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), 'Andorra')  # noqa: E501
        self.assertIsNone(rapidfuzz_set.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))
        self.assertEqual(rapidfuzz_set.fuzzy_get('Gondor', strategy=Strategy.FIRST, score_cutoff=61), 'Andorra')  # noqa: E501

    def test_get_fuzzy_scores(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_set = RapidFuzzSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        def _check(item) -> bool:
            return item[1] is not None

        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('Australia', score_cutoff=100))), { ( 'Australia', 100.0, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('   aUstraLia  ', score_cutoff=100))), { ( 'Australia', 100.0, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('Austraia'))), { ( 'Australia', 94.11764705882352, ), ( 'Austria', 93.33333333333333, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('Ustralia'))), { ( 'Australia', 94.11764705882352, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('Austria'))), { ( 'Austria', 100.0, ), })
        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('Gondor'))), set())
        self.assertSetEqual(set(filter(_check, rapidfuzz_set.get_fuzzy_scores('Gondor', score_cutoff=60))), { ( 'Andorra', 61.53846153846154, ), ( 'El Salvador', 60.00000000000001, ), ( 'Norfolk Island', 60.00000000000001, ), ( 'Northern Mariana Islands', 60.00000000000001, ), ( 'Republic of North Macedonia', 60.00000000000001, ), ( 'Togo', 60.00000000000001, ), })  # noqa: E501

    def test_get_fuzzy_score_iter(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_set = RapidFuzzSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        targets = { ( 'Australia', 100.0, ), }
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('Australia', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 100.0, ), }
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('   aUstraLia  ', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, ), ( 'Austria', 93.33333333333333, ), }
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('Austraia'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, ), }
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('Ustralia'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Austria', 100.0, ), }
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('Austria'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = set()
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('Gondor'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Andorra', 61.53846153846154, ), ( 'El Salvador', 60.00000000000001, ), ( 'Norfolk Island', 60.00000000000001, ), ( 'Northern Mariana Islands', 60.00000000000001, ), ( 'Republic of North Macedonia', 60.00000000000001, ), ( 'Togo', 60.00000000000001, ), }  # noqa: E501
        source = set()
        for choice, score in rapidfuzz_set.get_fuzzy_score_iter('Gondor', score_cutoff=60):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)
