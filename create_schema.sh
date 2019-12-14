#!/bin/bash

echo "Creating user itc..."
echo "Enter your password to root database: "
PASS=$(grep \'password\': config.py | awk '{print $NF}' | grep -o -E '\w+')
PASS="$PASS" envsubst < create_user.sql > create_user-tmp.sql
mysql -h 127.0.0.1 -P 3306 -u root -p < create_user-tmp.sql
rm create_user-tmp.sql

echo "Creating schema..."
mysql -h 127.0.0.1 -P 3306 -u itc --password="$PASS" < create_table.sql
