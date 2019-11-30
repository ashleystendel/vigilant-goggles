import json
import mysql.connector
from mysql.connector import errorcode


class Database:
    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
            sql_config = data.mysql

        try:
            self.db = mysql.connector.connect(**sql_config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.cursor = self.db.cursor()

    def insert_rows(self, table, data):
        """
        Takes a table name and a list of tuples. Inserts each tuple as a row
        in the database. Returns a success status upon completion, otherwise
        returns an error
        """
        ## defining the Query
        query = f"REPLACE INTO {table} {data}"
        ## executing the query with data provided
        for datum in data:
            self.cursor.execute(query, datum)
        return
