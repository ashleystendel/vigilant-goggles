#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import argparse
import config
from page_parser import PageParser
from question_summary import QuestionSummary
from tag import Tag
from database_connection import Database


def update_tag_table(db, url):
    """
    updates Tag database table
    :param db: database object
    :param url: url to scrape
    """
    print("Updating DB")
    tag_parser = PageParser(url, "tags?page=")
    tags = tag_parser.get_pages(Tag, 9999)
    db.insert_tags(tags)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pages', type=int)
    parser.add_argument('--url', type=str)
    parser.add_argument('--update_tag_db', '-u', help='Upsert scraped data to database', required=False)
    args = parser.parse_args()

    results = {}

    db = Database()

    if db.is_empty('Tag'):
        print("Empty DB")
        update_tag_table(db, args.url)

    if args.update_tag_db:
        update_tag_table(db, args.url)

    print("Getting Question Summaries")
    summary_parser = PageParser(args.url, "questions?tab=newest&page=")
    summaries = summary_parser.get_pages(QuestionSummary, args.num_pages)
    results['summaries'] = summaries
    db.insert_question_summaries(results['summaries'])


if __name__ == '__main__':
    main()
