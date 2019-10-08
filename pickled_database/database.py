# dill allows lambda function tests to be saved
import dill as pickle
import pathlib
import os
import pprint

from pickled_database.tested_setter_and_getter import TestedSetterAndGetter
import utils


class PickledDatabase:
    """
    I intend this database to be used across several files for accessing values.

    For best practice, all keys should be created in one file, they can then be used in multiple files.
    """

    def __init__(self, database_path="database.pkl"):
        self._path = database_path

    def create_key(self, key, value=None, tests=()):
        if key in self:
            raise KeyError("Key already exists")
        tests = utils.lists.make_sure_is_iterable(tests)

        db = self._load_database()
        db[key] = TestedSetterAndGetter(value, *tests)
        self._save_database(db)

    def set(self, key, value):
        if key not in self:
            raise KeyError("Create keys with the `create_key` method")
        db = self._load_database()
        db[key].set(value)
        self._save_database(db)

    def get(self, key):
        try:
            db = self._load_database()
            return db[key].get()
        except KeyError as e:
            raise e
        except ValueError as e:
            raise e

    def is_set(self, key):
        if key not in self:
            raise KeyError(f"'{key}' isn't in the database")
        db = self._load_database()
        return db[key].is_set

    def get_keys(self):
        db = self._load_database()
        return list(db.keys())

    def __contains__(self, item):
        return item in self.get_keys()

    def delete_key(self, key):
        db = self._load_database()
        try:
            db.pop(key)
        except KeyError:
            pass
        self._save_database(db)

    def clear_database(self):
        self._save_database(dict())

    def delete_database_file(self):
        os.remove(self._path)  # cleanup the created file

    def _load_database(self):
        if not pathlib.Path(self._path).exists():
            return dict()
        else:
            with open(self._path, 'rb') as f:
                db = pickle.load(f)
            return db

    def _save_database(self, db):

        directory = os.path.dirname(self._path)
        if directory is not '':
            os.makedirs(directory, exist_ok=True)

        with open(self._path, 'wb') as f:
            pickle.dump(db, f)

    def __repr__(self):
        return pprint.pformat(
            self._get_dictionary(
                is_show_unset=True,
            ),
            width=1
        )

    def _get_dictionary(self, is_show_unset=False, unset_display_value=None):
        db_dict = dict()
        for key in self.get_keys():
            try:
                value = self.get(key)
            except ValueError:
                if is_show_unset:
                    value = unset_display_value
                else:
                    continue
            db_dict[key] = value
        return db_dict


if __name__ == '__main__':

    path = "pickled_database.pkl"
    db1 = PickledDatabase(path)
    db1.clear_database()

    # Any database referencing the same file will always have the same state
    db2 = PickledDatabase(path)

    db2.create_key('key1')

    db2.create_key('key2')
    db2.set('key2', 'value')
    assert db2.get('key2') == 'value'

    # create a key with a value
    db2.create_key('key3', 4)

    # create a key with value and a test for that value and all future set values
    db2.create_key('key4', 4, lambda x: type(x) is int)

    # if the test doesn't pass it isn't added
    try:
        db2.create_key('key5', 5, lambda x: type(x) is str)
    except ValueError:
        pass

    # create a key with multiple tests
    db2.create_key(
        'key6',
        6,
        [
            lambda x: type(x) is int,
            lambda x: x > 3,
        ]
    )
    try:
        # Will fail because it doesn't pass the tests
        db2.set('key6', 1)
    except ValueError:
        pass

    # create a key with a test and no value
    db2.create_key('key7', tests=lambda x: type(x) is str)
    db2.set('key7', 'hi')
    try:
        db2.set('key7', 1)
    except ValueError:
        pass

    # create and delete keys
    db2.create_key('key8')
    db2.delete_key('key8')

    # you can't create keys multiple times
    db2.create_key('key9')
    try:
        db2.create_key('key9')
    except KeyError:
        pass

    # print the database with pretty print, tests aren't displayed
    print(db1)
    print("Note that 'None' is filled in for keys that don't have a value for visualization")

    # you can delete the database file, if you like
    db1.delete_database_file()
