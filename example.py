from pickled_database import PickledDatabase
import datetime
import os


path = "pickled_database.pkl"
db1 = PickledDatabase(path)
assert os.path.exists(path)  # file is created on initialization
db1.clear_database()

# Any database referencing the same file will always have the same state
db2 = PickledDatabase(path)

db2.create_key('key1')

db2.create_key('key2')
db2.set('key2', 'value')
assert db2.get('key2') == 'value'

# create a key with a value
db2.create_key('key3', 3)
# check when a key was last set
assert datetime.datetime.now() > db2.get_last_set('key3')

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
