#!/bin/sh

cd tests/testproject/
mkdir static
./manage.py migrate
./manage.py test
rm test_db.sqlite3
rmdir static
