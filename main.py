#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import argparse
from api_parser import APIParser
from page_parser import PageParser
from question_summary import QuestionSummary
from tag import Tag
from database_connection import Database
from article import Article
from logger import Logger

MAX = 9999
args = {'debug' : True}
log = Logger(args)


def update_tag_table(db):
    """
    updates Tag database table
    :param db: database object
    """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pages', type=int)
    parser.add_argument('--update_tag_db', '-u', help='Upsert scraped data to database',
                        required=False, action='store_true')
    args = parser.parse_args()

    db = Database()
    if db.is_empty('Tag') or args.update_tag_db:
        tag_parser = PageParser("tag")
        tags = tag_parser.get_pages(Tag, MAX)
        db.update_tag_table(tags)

    log.logger.warning("Getting Question Summaries...")
    print("Getting Question Summaries...")
    summary_parser = PageParser("question_summary")
    summaries = summary_parser.get_pages(QuestionSummary, args.num_pages)

    print("Getting Articles...")
    article_parser = APIParser()
    articles = article_parser.get_responses(Article, summaries)

    #Enrich Question Summary with articles
    for question_summary, articles_list in zip(summaries, articles):
        question_summary.add_articles(articles_list)

    print("Populating DB...")
    db.insert_question_summaries(summaries)

if __name__ == '__main__':
    main()
