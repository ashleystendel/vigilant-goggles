#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import sys
import argparse

from page_parser import PageParser
from question_summary import QuestionSummary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('page_type', choices=['questions', 'users'], type=str)
    parser.add_argument('--num_pages', type=int)
    parser.add_argument('-s', action='store_true')
    args = parser.parse_args()

    if args.num_pages is None:
        args.num_pages = 1

    results = {}
    if args.page_type == 'questions':
        summary_parser = PageParser("https://medicalsciences.stackexchange.com/questions?tab=newest&page=")
        summaries = summary_parser.get_pages(QuestionSummary, args.num_pages)
        results['summaries'] = summaries


if __name__ == '__main__':
    main()