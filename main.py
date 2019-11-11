#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
from helper_functions import *


def main():
    
    summary_parser = PageParser("https://medicalsciences.stackexchange.com/")
    summaries = find_and_populate(summary_parser, "div", "question-summary", 'QuestionSummary')

    user_page_parser = PageParser('https://medicalsciences.stackexchange.com/users')
    users = find_and_populate(user_page_parser, "div", "grid-layout--cell user-info  user-hover", 'User')


if __name__ == '__main__':
    main()
