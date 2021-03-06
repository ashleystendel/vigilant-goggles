#!/bin/bash

echo "Creating user itc..."
echo "Enter your password to root database: "
PASS=$(grep \'password\': config.py | awk '{print $NF}' | grep -o -E '\w+')
PASS="$PASS" envsubst < create_user.sql > create_user-tmp.sql
sudo mysql -h localhost -P 3306 -u root -p < create_user-tmp.sql
rm create_user-tmp.sql

echo "Creating schema..."
sudo mysql -h localhost -P 3306 -u itc --password="$PASS" < create_table.sql
