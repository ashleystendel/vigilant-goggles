CREATE USER IF NOT EXISTS 'itc'@'localhost' IDENTIFIED BY '$PASS';

GRANT CREATE, SELECT, INSERT, UPDATE, REFERENCES ON vgdb . * TO 'itc'@'localhost';
