#!/bin/bash

echo "Creating user itc..."

PASS="$(cat password.txt)" envsubst < create_user.sql > create_user-tmp.sql
mysql --datadir='~/test/' -h 127.0.0.1 -P 3306 -u root -p < create_user-tmp.sql
rm create_user-tmp.sql

echo "Creating schema..."
mysql --datadir='~/test/' -h 127.0.0.1 -P 3306 -u itc -p < create_table.sql
