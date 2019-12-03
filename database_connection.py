import json
import mysql.connector
from mysql.connector import errorcode
import datetime
import inflection


class Database:
    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
            sql_config = data['mysql']

        try:
            self.db = mysql.connector.connect(**sql_config, use_pure=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.cursor = self.db.cursor()

    def update_helper(self, d, columns):
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

    def check(self, table, val, key):
        if type(val) != str:
            val = getattr(val, key)

        check = f"SELECT id{table} FROM {table} WHERE {key} = %s"
        self.cursor.execute(check, (val,))
        res = self.cursor.fetchone()
        if res:
            res = res[0]
        return res

    def insert(self, table, columns, tup, date):
        query = f"INSERT INTO {table}({columns})\
                        VALUES {tup + (date,)}"
        self.cursor.execute(query)

    def update(self, table, fields, date, val):
        query = f"UPDATE {table} SET \
                {fields} dateScraped = '{date}' \
                WHERE id{table} = {val}"

        self.cursor.execute(query)

    def upsert(self, d, date, key, table, columns, to_del=""):
        tup = d.convert_to_tuple(to_del)
        res = self.check(table, d, key)

        if not res:
            self.insert(table, columns, tup, date)
        else:
            fields = self.update_helper(d, columns)
            self.update(table, fields, date, res)
        self.db.commit()

    def insert_tags(self, data):
        date = str(datetime.datetime.now())

        for d in data:
            self.upsert(d, date, "name", "Tag", "name, countDay, countWeek, countMonth, countYear, totalCount, dateScraped")

    def insert_question_summaries(self, data):
        date = str(datetime.datetime.now())

        for d in data:
            self.upsert(d, date, "ref", "QuestionSummary",
                        "ref, voteCount, answerCount, viewCount, question, datePosted, dateScraped", "tags")
            self.cursor.execute(f"SELECT idQuestionSummary FROM QuestionSummary WHERE ref = '{d.ref}'")
            qs_id = self.cursor.fetchone()[0]

            for tag in d.tags:
                tag_id = self.check("Tag", tag, "name")
                query = f"SELECT idAssociatedTag FROM AssociatedTag WHERE tagId = {tag_id} and questionSummaryId = {qs_id}"

                self.cursor.execute(query)
                res = self.cursor.fetchone()
                if not res:
                    query = f"INSERT INTO AssociatedTag(tagId, questionSummaryId) VALUES ({tag_id}, {qs_id})"
                    self.cursor.execute(query)