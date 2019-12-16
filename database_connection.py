import mysql.connector
from mysql.connector import errorcode
import datetime
import inflection

from associated_article import AssociatedArticle
from associated_tag import AssociatedTag
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

    def update_helper(self, d, columns, date=()):
        """
        Creates UPDATE section of SQL UPDATE query string
        from database column names and associated object
        <attr1> = <val1>, <attr2> = <val2> ....
        :param d: object with values to update in database
        :param columns: string of table column names
        :return: string of update section for SQL update
        """
        # Only add date scraped if in columns from table (Associated* does not have date)
        cols = columns.copy()
        res = ""
        if 'dateScraped' in cols:
            cols.remove('dateScraped')
            res = f"dateScraped = \"{date}\", "

        #Convert camel case database column names to underscore for object
        fields = list(map((lambda x: inflection.underscore(x)), cols))

        for field, col in zip(fields, cols):
            val = getattr(d, field)
            res += f"{col} = {self.get_val(val)}, "

        return res.rstrip(", ")

    def get_column_names(self, table):
        """
        gets column names from table
        :param table: table name
        :return: list of column names
        """
        query = f"SHOW COLUMNS IN {table}"
        self.cursor.execute(query)
        cols_info = self.cursor.fetchall()[1:]
        return [t[0] for t in cols_info]

    def get_val(self, s):
        """
        returns properly parametrized for sql statement
        :param s: value either int, float or string
        :return: parametrized value
        """
        if type(s) == int or type(s) == float:
            return s
        else:
            return f"\"{s}\""

    def check(self, table, obj, cols=[]):
        """
        Checks if an entry is the table.
        Performs SELECT <id> FROM <table> WHERE <attr1> = <val1> ...
        for every attribute in object.
        if cols is specified, only queries those specific attributes
        :param table: table name
        :param obj: object with value(s) to be searched
        :return: id for value being searched for or None
        """
        if not cols:
            columns = self.get_column_names(table)
            cols = columns.copy()

        if "dateScraped" in cols:
            cols.remove("dateScraped")
        vals = [getattr(obj, inflection.underscore(key)) for key in cols]

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
        if not res:
            print("Empty DB...")
            return True

        return False

    def update_tag_table(self, tags):
        """
        Update tags database with all pages of tags
        :param tags: list of all tags
        """
        print("Updating DB...")
        self.insert_tags(tags)

    def insert(self, table, tup, date):
        """
        inserts data into table
        :param table: table name
        :param tup: tuple of data to be inserted
        :param date: date as string
        """
        if not date == ():
            tup = tup + (date,)
        columns = ", ".join(self.get_column_names(table))
        query = f"INSERT INTO {table}({columns})\
                        VALUES {tup}"

        self.cursor.execute(query)

    def update(self, table, fields, primary_key):
        """
        update a row in table with values with row id
        :param table: table name
        :param fields: string of update section for SQL update
        :param date: date as string
        :param primary_key: primary key value
        :return:
        """
        query = f"UPDATE {table} SET \
                {fields} \
                WHERE id{table} = {primary_key}"
        self.cursor.execute(query)

    def upsert(self, obj, table, date=(), to_del=[], cols=[]):
        """
        performs an insert if data is not in table or an update if it is present
        :param obj: object with values to update in database
        :param table: table name
        :param date: (Optional) date as string
        :param to_del: (Optional) field to remove from object before insertion into data
        :param cols:  (Optional) attributes of table to query over
        """
        tup = obj.convert_to_tuple(to_del)
        columns = self.get_column_names(table)
        res = self.check(table, obj, cols)

        if not res:
            self.insert(table, tup, date)
        else:
            fields = self.update_helper(obj, columns, date)
            self.update(table, fields, res)
        self.db.commit()

    def insert_articles(self, data):
        """
        insert list of Acticle objects into Article table
        :param data: list of Articles
        """
        date = str(datetime.datetime.now())

        for row in data:
            self.upsert(row, "Article", date)

    def insert_tags(self, data):
        """
        inserts list of Tag objects into Tag table
        :param data: list of Tag objects
        """
        date = str(datetime.datetime.now())

        for row in data:
            self.upsert(row, "Tag", date)

    def insert_question_summaries(self, data):
        """
        inserts QuestionSummary objects into QuestionSummary table
        :param data: list of QuestionSummary objects
        """
        date = str(datetime.datetime.now())

        for row in data:
            tags = row.tags
            articles = row.articles

            self.upsert(row, "QuestionSummary", date, ['tags', 'articles'], ['ref', 'question'])
            self.insert_articles(articles)

            qs_id = self.check("QuestionSummary", row)

            for tag in tags:
                tag_id = self.check("Tag", tag, ['name'])
                ass_tag = AssociatedTag(tag_id, qs_id)

                self.upsert(ass_tag, "AssociatedTag")

            for article in articles:
                article_id = self.check("Article", article)
                ass_tag = AssociatedArticle(article_id, qs_id)

                self.upsert(ass_tag, "AssociatedArticle")


