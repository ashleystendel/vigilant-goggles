#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import argparse

from page_parser import PageParser
from question_summary import QuestionSummary
from tag import Tag
from database_connection import Database


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pages', type=int)
    parser.add_argument('--update_db', '-u', help='Upsert scraped data to database')
    args = parser.parse_args()

    if args.num_pages is None:
        args.num_pages = 1

    results = {}

    db = Database()

    tag_parser = PageParser("https://medicalsciences.stackexchange.com/tags?page=")
    tags = tag_parser.get_pages(Tag, 1)
    results['tags'] = tags
    db.insert_tags(results['tags'])

    summary_parser = PageParser("https://medicalsciences.stackexchange.com/questions?tab=newest&page=")
    summaries = summary_parser.get_pages(QuestionSummary, args.num_pages)
    results['summaries'] = summaries
    db.insert_question_summaries(results['summaries'])

    if args.update_db:
        pass


if __name__ == '__main__':
    main()
