README
======

[![Build Status](https://travis-ci.com/robotpt/pickle-database.svg?branch=master)](https://travis-ci.com/robotpt/pickle-database)
[![Downloads](https://pepy.tech/badge/pickle-database)](https://pepy.tech/project/pickle-database)

A database that saves its state in a file every time it is modified.
See `example.py` for usage.

Features:

* Allows `0` to `n` tests to be run on setting a variable.  If these tests don't pass, an exception is raised.
* Records the time that a database key is last set.  

Setup
-----

### Option 1: Clone the repository

> Best if you want to modify or view the code - note that you can do the following inside of a virtual environment

    git clone https://github.com/robotpt/pickle-database
    
An easy way to setup the repository with its dependencies and with your Python path
is to use `pip`.  

    pip install -e pickle-database

Tests can be run with the following commands.
    
    cd pickle-database
    python3 -m unittest

### Option 2: Use Pip

> Best if you just want to use it

    python3 -m pip install pickle_database
