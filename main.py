#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import sys
from helper_functions import *
import argparse



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
        summaries = []
        for i in range (args.num_pages):
            summary_parser = PageParser(f"https://medicalsciences.stackexchange.com/questions?tab=newest&page={i}")
            summaries.append(find_and_populate(summary_parser, "div", "question-summary", 'QuestionSummary'))
        results["question_summaries"] = summaries

    if args.page_type == 'users':
        users = []
        for i in range (args.num_pages):
            user_page_parser = PageParser(f"https://medicalsciences.stackexchange.com/users?page={i}&tab=reputation&filter=month")
            users.append(find_and_populate(user_page_parser, "div", "grid-layout--cell user-info  user-hover", 'User'))
        results["users"] = users

    if args.s:
        with open('results.csv', w):
            a = 3

    print(results)

if __name__ == '__main__':
    main()
