
import operator

from copy import copy
from rapidfuzz.distance import Levenshtein
from unittest import TestCase

from rapidfuzz_collections import (
    Normalizer,
    ScorerType,
    Strategy,
    RapidFuzzFrozenSet
)

from data import data_tuple


# noinspection DuplicatedCode
class TestRapidFuzzFrozenSet(TestCase):

    def test__init__(self):
        seq = { 'test1', 'test2', }
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)

        rapidfuzz_frozenset = RapidFuzzFrozenSet(
            seq,
            normalizer=normalizer,
            score_cutoff=2,
            score_hint=1,
            scorer=Levenshtein.distance,  # noqa
            scorer_kwargs={ 'weights': ( 1, 2, 1, ), },
            scorer_type=ScorerType.DISTANCE,
            strategy=Strategy.BEST_ONLY_ONE
        )

        self.assertIsInstance(rapidfuzz_frozenset, RapidFuzzFrozenSet)

    def test__and__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, None)
        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, 'test1')
        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, 1)
        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, 1.1)
        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.and_, rapidfuzz_frozenset1, { 'k1': 'k2', })

        rapidfuzz_frozenset2 = rapidfuzz_frozenset1 & RapidFuzzFrozenSet({ 'test3', 'test4', })
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 'test3', })

        rapidfuzz_frozenset3 = rapidfuzz_frozenset1 & { 'test3', 'test4', }
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 'test3', })

        rapidfuzz_frozenset4 = rapidfuzz_frozenset1 & frozenset({ 'test3', 'test4', })
        self.assertSetEqual(set(rapidfuzz_frozenset4), { 'test3', })

    def test__contains__(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 1, })

        self.assertTrue('test2' in rapidfuzz_frozenset)
        self.assertFalse('test3' in rapidfuzz_frozenset)

    def test__copy__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ ( 'test1', ), })
        rapidfuzz_frozenset2 = copy(rapidfuzz_frozenset1)

        self.assertSetEqual(rapidfuzz_frozenset1._data, rapidfuzz_frozenset2._data)
        self.assertIs(rapidfuzz_frozenset1._data, rapidfuzz_frozenset2._data)

    def test__eq__(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 'test1', })

        self.assertFalse(rapidfuzz_frozenset == RapidFuzzFrozenSet({ 'test3', 'test4', }))
        self.assertTrue(rapidfuzz_frozenset == RapidFuzzFrozenSet({ 'test1', 'test2', }))
        self.assertFalse(rapidfuzz_frozenset == { 'test5', 'test6', })
        self.assertFalse(rapidfuzz_frozenset == { 'test1', 'test2', })
        self.assertFalse(rapidfuzz_frozenset == frozenset({ 'test5', 'test6', }))
        self.assertFalse(rapidfuzz_frozenset == frozenset({ 'test1', 'test2', }))

    def test__iter__(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', })

        seq = { i for i in rapidfuzz_frozenset }

        self.assertSetEqual(seq, { 'test1', 'test2', })

    def test__len__(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 1, })

        self.assertEqual(len(rapidfuzz_frozenset), 3)

    def test__ne__(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 'test1', })

        self.assertTrue(rapidfuzz_frozenset != RapidFuzzFrozenSet({ 'test3', 'test4', }))
        self.assertFalse(rapidfuzz_frozenset != RapidFuzzFrozenSet({ 'test1', 'test2', }))
        self.assertTrue(rapidfuzz_frozenset != { 'test5', 'test6', })
        self.assertTrue(rapidfuzz_frozenset != { 'test1', 'test2', })
        self.assertTrue(rapidfuzz_frozenset != frozenset({ 'test5', 'test6', }))
        self.assertTrue(rapidfuzz_frozenset != frozenset({ 'test1', 'test2', }))

    def test__or__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })

        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, None)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, 'test1')
        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, 1)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, 1.1)
        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.or_, rapidfuzz_frozenset1, { 'k1': 'k2', })

        rapidfuzz_frozenset2 = rapidfuzz_frozenset1 | { 'test2', 'test4', 2, }
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset2.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

        rapidfuzz_frozenset3 = rapidfuzz_frozenset1 | frozenset({ 'test2', 'test4', 2, })
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset3.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

        rapidfuzz_frozenset4 = rapidfuzz_frozenset1 | RapidFuzzFrozenSet({ 'test3', 'test4', 2, })
        self.assertSetEqual(set(rapidfuzz_frozenset4), { 1, 2, 'test2', 'test4', '  test1  ', 'test1', 'test3', })
        self.assertDictEqual(rapidfuzz_frozenset4.choices, { None: { 1, 2, }, 'test2': { 'test2', }, 'test4': { 'test4', }, 'test1': { '  test1  ', 'test1', }, 'test3': {'test3'}, })  # noqa: E501

    def test__rand_(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, operator.and_, None, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.and_, 'test1', rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.and_, 1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.and_, 1.1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.and_, ( 1, 2, ), rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.and_, [ 1, 2, ], rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.and_, { 'k1': 'k2', }, rapidfuzz_frozenset1)

        rapidfuzz_frozenset2 = { 'test3', 'test4', } & rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 'test3', })

        rapidfuzz_frozenset3 = frozenset({ 'test3', 'test4', }) & rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 'test3', })

    def test__repr__(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', })

        self.assertEqual(repr(rapidfuzz_frozenset), "RapidFuzzFrozenSet(frozenset({'test1'}))")

    def test__ror__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 1, 'test1', '  test1  ', })

        self.assertRaises(TypeError, operator.or_, None, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.or_, 'test1', rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.or_, 1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.or_, 1.1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.or_, ( 1, 2, ), rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.or_, [ 1, 2, ], rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.or_, { 'k1': 'k2', }, rapidfuzz_frozenset1)

        rapidfuzz_frozenset2 = { 'test2', 'test4', 2, } | rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset2.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

        rapidfuzz_frozenset3 = frozenset({ 'test2', 'test4', 2, }) | rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 'test2', 1, 2, '  test1  ', 'test4', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset3.choices, { 'test2': { 'test2', }, None: { 1, 2, }, 'test1': { 'test1', '  test1  ', }, 'test4': { 'test4', }, })  # noqa: E501

    def test__rsub__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.sub, None, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.sub, 'test1', rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.sub, 1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.sub, 1.1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.sub, [ 1, 2, ], rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.sub, ( 1, 2, ), rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.sub, { 'k1': 'k2', }, rapidfuzz_frozenset1)

        rapidfuzz_frozenset2 = { 'test3', 'test2', } - rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 'test3', })
        self.assertDictEqual(rapidfuzz_frozenset2.choices, { 'test3': { 'test3', }, })

        rapidfuzz_frozenset3 = frozenset({ 'test3', 'test2', }) - rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 'test3', })
        self.assertDictEqual(rapidfuzz_frozenset3.choices, { 'test3': { 'test3', }, })

    def test__rxor__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.xor, None, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.xor, 'test1', rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.xor, 1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.xor, 1.1, rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.xor, [ 1, 2, ], rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.xor, ( 1, 2, ), rapidfuzz_frozenset1)
        self.assertRaises(TypeError, operator.xor, { 'k1': 'k2', }, rapidfuzz_frozenset1)

        rapidfuzz_frozenset2 = { 'test3', 'test2', } ^ rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset2.choices, { None: { 1, }, 'test3': { 'test3', }, 'test1': { 'test1', }, })  # noqa: E501

        rapidfuzz_frozenset3 = frozenset({ 'test3', 'test2', }) ^ rapidfuzz_frozenset1
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset3.choices, { None: { 1, }, 'test3': { 'test3', }, 'test1': { 'test1', }, })  # noqa: E501

    def test__sub__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, None)
        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, 'test1')
        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, 1)
        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, 1.1)
        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.sub, rapidfuzz_frozenset1, { 'k1': 'k2', })

        rapidfuzz_frozenset2 = rapidfuzz_frozenset1 - { 'test3', 'test2', }
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_frozenset2.choices, { 'test1': { 'test1', }, None: { 1, }, })

        rapidfuzz_frozenset3 = rapidfuzz_frozenset1 - frozenset({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_frozenset3.choices, { 'test1': { 'test1', }, None: { 1, }, })

        rapidfuzz_frozenset4 = rapidfuzz_frozenset1 - RapidFuzzFrozenSet({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_frozenset4), { 'test1', 1, })
        self.assertDictEqual(rapidfuzz_frozenset4.choices, { 'test1': { 'test1', }, None: { 1, }, })

    def test__xor__(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ 'test1', 'test2', 1, })

        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, None)
        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, 'test1')
        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, 1)
        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, 1.1)
        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, [ 1, 2, ])
        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, ( 1, 2, ))
        self.assertRaises(TypeError, operator.xor, rapidfuzz_frozenset1, { 'k1': 'k2', })

        rapidfuzz_frozenset2 = rapidfuzz_frozenset1 ^ { 'test3', 'test2', }
        self.assertSetEqual(set(rapidfuzz_frozenset2), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset2.choices, { None: { 1, }, 'test1': { 'test1', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_frozenset3 = rapidfuzz_frozenset1 ^ frozenset({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_frozenset3), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset3.choices, { None: { 1, }, 'test1': { 'test1', }, 'test3': { 'test3', }, })  # noqa: E501

        rapidfuzz_frozenset4 = rapidfuzz_frozenset1 ^ RapidFuzzFrozenSet({ 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_frozenset4), { 1, 'test3', 'test1', })
        self.assertDictEqual(rapidfuzz_frozenset4.choices, { None: { 1, }, 'test1': { 'test1', }, 'test3': { 'test3', }, })  # noqa: E501

    def test_choices(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ '  tEst1', 'teSt2  ', 't3', '  t4  ', 1, 1.1, None, })

        self.assertDictEqual(rapidfuzz_frozenset.choices, { None: { None, 1, 1.1, '  t4  ', 't3'}, 'tEst1': { '  tEst1', }, 'teSt2': { 'teSt2  ', }, })  # noqa: E501

    def test_copy(self):
        rapidfuzz_frozenset1 = RapidFuzzFrozenSet({ ( 'test1', ), })
        rapidfuzz_frozenset2 = copy(rapidfuzz_frozenset1)

        self.assertSetEqual(rapidfuzz_frozenset1._data, rapidfuzz_frozenset2._data)
        self.assertIs(rapidfuzz_frozenset1._data, rapidfuzz_frozenset2._data)

    def test_difference(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.difference({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_frozenset.difference(RapidFuzzFrozenSet({ 'test1', 'test4', }))), { 'test3', 'test2', })  # noqa: E501
        self.assertSetEqual(set(rapidfuzz_frozenset.difference({ 'test1', 'test4', })), { 'test3', 'test2', })
        self.assertSetEqual(set(rapidfuzz_frozenset.difference({ 'test1', 'test4', }, { 'test2', 'test5', })), { 'test3', })  # noqa: E501

    def test_intersection(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.intersection({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_frozenset.intersection(RapidFuzzFrozenSet({ 'test1', 'test4', }))), { 'test1', })  # noqa: E501
        self.assertSetEqual(set(rapidfuzz_frozenset.intersection({ 'test1', 'test4', })), { 'test1', })
        self.assertSetEqual(set(rapidfuzz_frozenset.intersection({ 'test2', 'test4', }, { 'test2', 'test5', })), { 'test2', })  # noqa: E501

    # noinspection PyTypeChecker
    def test_isdisjoint(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.isdisjoint({ 'k1': 'k2', }))

        self.assertTrue(rapidfuzz_frozenset.isdisjoint(RapidFuzzFrozenSet({ 'test3', 'test4', })))
        self.assertTrue(rapidfuzz_frozenset.isdisjoint({ 'test3', 'test4', }))
        self.assertFalse(rapidfuzz_frozenset.isdisjoint(RapidFuzzFrozenSet({ 'test1', 'test4', })))
        self.assertFalse(rapidfuzz_frozenset.isdisjoint({ 'test1', 'test4', }))

    # noinspection PyTypeChecker
    def test_issubset(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issubset({ 'k1': 'k2', }))

        self.assertTrue(rapidfuzz_frozenset.issubset(RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })))
        self.assertTrue(rapidfuzz_frozenset.issubset({ 'test1', 'test2', 'test3', }))
        self.assertFalse(rapidfuzz_frozenset.issubset(RapidFuzzFrozenSet({ 'test11', 'test22', 'test3', })))
        self.assertFalse(rapidfuzz_frozenset.issubset({ 'test11', 'test22', 'test3', }))

    # noinspection PyTypeChecker
    def issuperset(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.issuperset({ 'k1': 'k2', }))

        self.assertTrue(rapidfuzz_frozenset.issuperset(RapidFuzzFrozenSet({ 'test2', 'test3', })))
        self.assertTrue(rapidfuzz_frozenset.issuperset({ 'test2', 'test3', }))
        self.assertFalse(rapidfuzz_frozenset.issuperset(RapidFuzzFrozenSet({ 'test1', 'test22', 'test3', })))
        self.assertFalse(rapidfuzz_frozenset.issuperset({ 'test1', 'test22', 'test3', }))

    # noinspection PyTypeChecker
    def test_symmetric_difference(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', 'test3', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.symmetric_difference({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_frozenset.symmetric_difference(RapidFuzzFrozenSet({ 'test1', 'test4', }))), { 'test4', 'test3', 'test2', })  # noqa: E501
        self.assertSetEqual(set(rapidfuzz_frozenset.symmetric_difference({ 'test1', 'test4', })), { 'test4', 'test3', 'test2', })  # noqa: E501

    def test_union(self):
        rapidfuzz_frozenset = RapidFuzzFrozenSet({ 'test1', 'test2', })

        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union(None))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union('test1'))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union(1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union(1.1))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union([ 1, 2, ]))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union(( 1, 2, )))
        self.assertRaises(TypeError, lambda: rapidfuzz_frozenset.union({ 'k1': 'k2', }))

        self.assertSetEqual(set(rapidfuzz_frozenset.union(RapidFuzzFrozenSet({ 'test1', 'test3', }), { 'test2', 'test4', })), { 'test1', 'test2', 'test3', 'test4', })  # noqa: E501

    def test_fuzzy_contains(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_frozenset = RapidFuzzFrozenSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertTrue(rapidfuzz_frozenset.fuzzy_contains('Australia', score_cutoff=100))

        # exact normalized key contains
        self.assertTrue(rapidfuzz_frozenset.fuzzy_contains('   aUstraLia  ', score_cutoff=100))

        # similar key contains
        self.assertTrue(rapidfuzz_frozenset.fuzzy_contains('Austraia'))
        self.assertTrue(rapidfuzz_frozenset.fuzzy_contains('Ustralia'))
        self.assertFalse(rapidfuzz_frozenset.fuzzy_contains('Gondor'))
        self.assertTrue(rapidfuzz_frozenset.fuzzy_contains('Gondor', score_cutoff=60))
        self.assertFalse(rapidfuzz_frozenset.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=3))  # noqa: E501
        self.assertTrue(rapidfuzz_frozenset.fuzzy_contains('Gondor', scorer=Levenshtein.distance, scorer_type=ScorerType.DISTANCE, score_cutoff=4))  # noqa: E501

    def test_fuzzy_get(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_frozenset = RapidFuzzFrozenSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        # exact key contains
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Australia', score_cutoff=100), 'Australia')

        # exact normalized key contains
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('   aUstraLia  ', score_cutoff=100), 'Australia')

        # similar key contains
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Austraia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertIsNone(rapidfuzz_frozenset.fuzzy_get('Austraia', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIn(rapidfuzz_frozenset.fuzzy_get('Austraia', strategy=Strategy.FIRST), { 'Austria', 'Australia', })  # noqa: E501
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Ustralia', strategy=Strategy.FIRST_FROM_BEST), 'Australia')  # noqa: E501
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Ustralia', strategy=Strategy.BEST_ONLY_ONE), 'Australia')
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Ustralia', strategy=Strategy.FIRST), 'Australia')
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Austria', strategy=Strategy.FIRST_FROM_BEST), 'Austria')  # noqa: E501
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Austria', strategy=Strategy.BEST_ONLY_ONE), 'Austria')  # noqa: E501
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Austria', strategy=Strategy.FIRST), 'Austria')
        self.assertIsNone(rapidfuzz_frozenset.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST))
        self.assertIsNone(rapidfuzz_frozenset.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE))
        self.assertIsNone(rapidfuzz_frozenset.fuzzy_get('Gondor', strategy=Strategy.FIRST))
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Gondor', strategy=Strategy.FIRST_FROM_BEST, score_cutoff=60), 'Andorra')  # noqa: E501
        self.assertIsNone(rapidfuzz_frozenset.fuzzy_get('Gondor', strategy=Strategy.BEST_ONLY_ONE, score_cutoff=60))  # noqa: E501
        self.assertEqual(rapidfuzz_frozenset.fuzzy_get('Gondor', strategy=Strategy.FIRST, score_cutoff=61), 'Andorra')  # noqa: E501

    def test_get_fuzzy_scores(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_frozenset = RapidFuzzFrozenSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        def _check(item) -> bool:
            return item[1] is not None

        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('Australia', score_cutoff=100))), { ( 'Australia', 100.0, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('   aUstraLia  ', score_cutoff=100))), { ( 'Australia', 100.0, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('Austraia'))), { ( 'Australia', 94.11764705882352, ), ( 'Austria', 93.33333333333333, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('Ustralia'))), { ( 'Australia', 94.11764705882352, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('Austria'))), { ( 'Austria', 100.0, ), })  # noqa: E501
        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('Gondor'))), set())
        self.assertSetEqual(set(filter(_check, rapidfuzz_frozenset.get_fuzzy_scores('Gondor', score_cutoff=60))), { ( 'Andorra', 61.53846153846154, ), ( 'El Salvador', 60.00000000000001, ), ( 'Norfolk Island', 60.00000000000001, ), ( 'Northern Mariana Islands', 60.00000000000001, ), ( 'Republic of North Macedonia', 60.00000000000001, ), ( 'Togo', 60.00000000000001, ), })  # noqa: E501

    def test_get_fuzzy_score_iter(self):
        normalizer = Normalizer().isinstance_str().strip().casefold().min_length(3)
        rapidfuzz_frozenset = RapidFuzzFrozenSet(data_tuple, normalizer=normalizer, score_cutoff=90)

        targets = { ( 'Australia', 100.0, ), }
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('Australia', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 100.0, ), }
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('   aUstraLia  ', score_cutoff=100):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, ), ( 'Austria', 93.33333333333333, ), }
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('Austraia'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Australia', 94.11764705882352, ), }
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('Ustralia'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Austria', 100.0, ), }
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('Austria'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = set()
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('Gondor'):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)

        targets = { ( 'Andorra', 61.53846153846154, ), ( 'El Salvador', 60.00000000000001, ), ( 'Norfolk Island', 60.00000000000001, ), ( 'Northern Mariana Islands', 60.00000000000001, ), ( 'Republic of North Macedonia', 60.00000000000001, ), ( 'Togo', 60.00000000000001, ), }  # noqa: E501
        source = set()
        for choice, score in rapidfuzz_frozenset.get_fuzzy_score_iter('Gondor', score_cutoff=60):
            if score is not None:
                source.add(( choice, score, ))
        self.assertSetEqual(targets, source)
