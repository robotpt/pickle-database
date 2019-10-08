import unittest
from pickled_database.tested_setter_and_getter import TestedSetterAndGetter


class TestTestedSetterAndGetter(unittest.TestCase):

    def test_lazy_initialization(self):

        sg = TestedSetterAndGetter()
        self.assertRaises(
            ValueError,
            sg.get
        )

        sg.append_tests(lambda x: type(x) is int)
        for i in range(-10, 10):
            sg.set(i)
            self.assertEqual(
                i,
                sg.get()
            )
        for v in ['a', None, callable, [1, 2], []]:
            self.assertRaises(
                ValueError,
                sg.set,
                v
            )

        sg.clear_tests()
        for v in ['a', None, callable, [1, 2], []]:
            sg.set(v)
            self.assertEqual(
                v,
                sg.get()
            )

        self.assertTrue(sg.is_set)
        sg.reset_value()
        self.assertFalse(sg.is_set)
        self.assertRaises(
            ValueError,
            sg.get
        )

    def test_constructor_initialization(self):

        sg = TestedSetterAndGetter(
            1,
            lambda x: type(x) is int,
            lambda x: x > 0
        )
        self.assertEqual(
            1,
            sg.get()
        )
        for v in [-1, 0, 'a', None, callable, [1, 2], []]:
            self.assertRaises(
                ValueError,
                sg.set,
                v
            )
