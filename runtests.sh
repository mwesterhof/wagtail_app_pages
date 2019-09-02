#!/bin/sh

cd tests/testproject/
./manage.py migrate
./manage.py test
rm test_db.sqlite3
