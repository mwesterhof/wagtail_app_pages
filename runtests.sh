#!/bin/sh

set -e

cd tests/testproject/
mkdir static || true
./manage.py migrate
./manage.py test
rm test_db.sqlite3
rmdir static
