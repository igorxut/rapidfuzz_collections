
from unittest import TestCase

from rapidfuzz_collections import Normalizer


class TestNormalization(TestCase):

    def test_default(self):
        normalizer1 = Normalizer.default()
        normalizer2 = Normalizer().isinstance_str().strip().min_length(3)

        for value in (
            None,
            123,
            123.123,
            [ 'test', ],
            { 'test', },
            ( 'test', ),
            { 'test': 'test', },
            'test',
        ):
            self.assertEqual(normalizer1(value), normalizer2(value))

    def test_capitalize(self):
        normalizer = Normalizer().capitalize()
        for source, target in (
            ( None, None, ),
            ( 123, None, ),
            ( 123.123, None, ),
            ( [ 'test', ], None, ),
            ( { 'test', }, None, ),
            ( ( 'test', ), None, ),
            ( { 'test': 'test', }, None, ),
            ( '  teSt1 2 tesT3 ', "  test1 2 test3 ", ),
            ( 'teSt1 2 tesT3 ', "Test1 2 test3 ", ),
        ):
            self.assertEqual(normalizer(source), target)

    def test_casefold(self):
        normalizer = Normalizer().casefold()
        for source, target in (
            ( None, None, ),
            ( 123, None, ),
            ( 123.123, None, ),
            ( [ 'test', ], None, ),
            ( { 'test', }, None, ),
            ( ( 'test', ), None, ),
            ( { 'test': 'test', }, None, ),
            ( '  teSt1 2 tesT3 ', "  test1 2 test3 ", ),
            ( 'teSt1 2 tesT3 ', "test1 2 test3 ", ),
        ):
            self.assertEqual(normalizer(source), target)

    def test_endswith(self):
        pass
