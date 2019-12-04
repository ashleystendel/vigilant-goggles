import mysql.connector
from mysql.connector import errorcode
import datetime
import inflection
from associated_tag import AssociatedTag
from tag import Tag
import config

class Database:
    def __init__(self):
        sql_config = config.mysql
        try:
            self.db = mysql.connector.connect(**sql_config, use_pure=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.cursor = self.db.cursor(buffered=True)

    def update_helper(self, d, columns):
        """
        Converts db column names to object attributes and generates
        update string section of SQL update
        :param d: object with values to update in database
        :param columns: string of table column names
        :return: string of update section for SQL update
        """
        cols = columns.split(", ")[:-1]
        fields = list(map((lambda x: inflection.underscore(x)), cols))
        res = ""
        for field, col in zip(fields, cols):
            val = getattr(d, field)
            if type(val) == str:
                res += f"{col} = \'{val}\', "
            else:
                res += f"{col} = {val}, "

        return res

    def get_column_names(self, table):
        """
        gets column names from table
        :param table: table name
        :return: list of column names
        """
        query = f"SHOW COLUMNS IN {table}"
        self.cursor.execute(query)
        cols_info = self.cursor.fetchall()[1:]
        return ", ".join([t[0] for t in cols_info])

    def get_val(self, s):
        """
        returns properly parametrized for sql statement
        :param s: value either int, float or string
        :return: parametrized value
        """
        if type(s) == int or type(s) == float:
            return s
        else:
            return f"\'{s}\'"

    def check(self, table, obj, cols):
        """
        Checks if an entry is the table
        :param table: table name
        :param obj: object with value(s) to be searched
        :param cols: list of database columns to search over
        :return: id for value being searched for or None
        """
        vals = [getattr(obj, inflection.underscore(key)) for key in cols]
        values = vals.copy()
        update = f'{cols.pop(0)}={self.get_val(vals.pop(0))}'

        for k, v in zip(cols, vals):
            update += f' and {k}={self.get_val(v)}'
        check = f"SELECT id{table} FROM {table} WHERE {update}"

        self.cursor.execute(check)
        res = self.cursor.fetchone()
        if not res:
            return res
        return res[0]

    def is_empty(self, table):
        """
        checks if the database is populated
        :param table: table name
        :return: True if populated else False
        """
        check = f"SELECT * FROM {table}"
        self.cursor.execute(check)
        res = self.cursor.fetchone()
        if len(res) < 1:
            return True
        else:
            return False

    def insert(self, table, columns, tup, date=()):
        """
        inserts data into table
        :param table: table name
        :param columns: string of all column names
        :param tup: tuple of data to be inserted
        :param date: date as string
        """
        query = f"INSERT INTO {table}({columns})\
                        VALUES {tup + date}"
        self.cursor.execute(query)

    def update(self, table, fields, date, primary_key):
        """
        update a row in table with values with row id
        :param table: table name
        :param fields: string of update section for SQL update
        :param date: date as string
        :param primary_key: primary key value
        :return:
        """
        query = f"UPDATE {table} SET \
                {fields} dateScraped = '{date}' \
                WHERE id{table} = {primary_key}"

        self.cursor.execute(query)

    def upsert(self, obj, date, columns, table, to_del=""):
        """
        performs an insert if data is not in table or an update if it is present
        :param obj: object with values to update in database
        :param date: date as string
        :param columns: database columns
        :param table: table name
        :param to_del: (Optional) field to remove from object before insertion into data
        """
        tup = obj.convert_to_tuple(to_del)
        res = self.check(table, obj, columns)
        columns = self.get_column_names(table)

        if not res:
            self.insert(table, columns, tup, (date,))
        else:
            fields = self.update_helper(obj, columns)
            self.update(table, fields, date, res)
        self.db.commit()

    def insert_tags(self, data):
        """
        inserts Tag objects into Tag table
        :param data: list of Tag objects
        """
        date = str(datetime.datetime.now())

        for row in data:
            self.upsert(row, date, ["name"], "Tag")

    def insert_question_summaries(self, data):
        """
        inserts QuestionSummary objects into QuestionSummary table
        :param data: list of QuestionSummary objects
        """
        date = str(datetime.datetime.now())

        for row in data:
            self.upsert(row, date, ["ref"], "QuestionSummary", 'tags')
            qs_id = self.check("QuestionSummary", row, ["ref"])
            for tag in row.tags:
                tag_obj = Tag()
                tag_obj.name = tag
                tag_id = self.check("Tag", tag_obj, ["name"])
                ass_tag = AssociatedTag(tag_id, qs_id)
                res = self.check("AssociatedTag", ass_tag, ["tagId", "questionSummaryId"])

                if not res:
                    a_tag = AssociatedTag(tag_id, qs_id)
                    self.insert("AssociatedTag", "tagId, questionSummaryId", (tag_id, qs_id))