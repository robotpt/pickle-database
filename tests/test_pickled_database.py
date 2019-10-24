import unittest
import datetime
import os

from pickled_database.database import PickledDatabase


class TestPickledDatabaseA(unittest.TestCase):

    def setUp(self):
        self.file = 'test_db.pkl'
        self.db = PickledDatabase(self.file)
        self.db.clear_database()

    def tearDown(self) -> None:
        os.remove(self.file)

    def test_key_creation(self):
        for k in ['key1', 'key2']:
            self.db.create_key(k)
            self.assertTrue(k in self.db)
        self.assertFalse('key-foo' in self.db)

    def test_setting_keys(self):
        self.db.create_key('key1')
        self.db.set('key1', 1)
        self.assertEqual(1, self.db.get('key1'))

    def test_dont_allow_duplicate_keys(self):
        for k in ['key1', 'key2']:
            self.db.create_key(k)
            self.assertRaises(
                KeyError,
                self.db.create_key,
                k
            )

    def test_error_in_tests_from_create_key(self):
        self.db.create_key('key1', 1, lambda x: type(x) is int)
        self.assertRaises(
            ValueError,
            self.db.set,
            'key1',
            'error'
        )

        self.db.create_key('key2', 2, [
            lambda x: type(x) is int,
            lambda x: x > 0,
        ]
                           )
        self.assertRaises(
            ValueError,
            self.db.set,
            'key2',
            -1
        )

    def test_error_in_tests_from_setter(self):
        self.db.create_key('key1', tests=lambda x: type(x) is int)
        self.assertRaises(
            ValueError,
            self.db.set,
            'key1',
            'error'
        )

        self.db.create_key('key2', tests=[
            lambda x: type(x) is int,
            lambda x: x > 0,
        ]
                           )
        self.assertRaises(
            ValueError,
            self.db.set,
            'key2',
            -1
        )

    def test_key_fails_test_on_create_not_added(self):

        self.assertRaises(
            ValueError,
            self.db.create_key,
            'key1',
            1,
            lambda x: type(x) is str
        )
        self.assertFalse('key1' in self.db)

        self.assertRaises(
            ValueError,
            self.db.create_key,
            'key2',
            'hi',
            [
                lambda x: type(x) is str,
                lambda x: len(x) > 10,
            ]
        )
        self.assertFalse('key2' in self.db)

    def test_unset_key(self):
        self.assertRaises(
            KeyError,
            self.db.get,
            'foo'
        )

        self.db.create_key('key')
        self.assertRaises(
            ValueError,
            self.db.get,
            'key'
        )
        self.assertFalse(self.db.is_set('key'))
        self.db.set('key', 'hi')
        self.assertTrue(self.db.is_set('key'))

    def test_last_set(self):

        key = 'key'
        self.db.create_key(key)

        for _ in range(10):
            self.assertIsNone(
                self.db.get_last_set(key)
            )
            self.db.set(key, 1)
            self.assertIsNotNone(
                self.db.get_last_set(key)
            )
            self.assertGreaterEqual(
                datetime.datetime.now(),
                self.db.get_last_set(key)
            )
            self.db.clear_value(key)
            self.assertIsNone(
                self.db.get_last_set(key)
            )



