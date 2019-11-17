#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import argparse

from page_parser import PageParser
from question_summary import QuestionSummary
from tag import Tag


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('page_type', choices=['questions', 'tags'], type=str)
    parser.add_argument('--num_pages', type=int)
    args = parser.parse_args()

    if args.num_pages is None:
        args.num_pages = 1

    results = {}
    if args.page_type == 'questions':
        summary_parser = PageParser("https://medicalsciences.stackexchange.com/questions?tab=newest&page=")
        summaries = summary_parser.get_pages(QuestionSummary, args.num_pages)
        results['summaries'] = summaries
        print(list(map((lambda x: x.__dict__), summaries)))

    if args.page_type == 'tags':
        tag_parser = PageParser("https://medicalsciences.stackexchange.com/tags?page=")
        tags = tag_parser.get_pages(Tag, args.num_pages)
        results['tags'] = tags
        print(list(map((lambda x: x.__dict__), tags)))


if __name__ == '__main__':
    main()
