""" Author: Jacob Mooney and Ashley Stendel
    This program scrapes https://medicalsciences.stackexchange.com/ """
from page_parser import *


def main():
    parser = PageParser("https://medicalsciences.stackexchange.com/")
    questions = parser.get_question_summaries()
    for question in questions:
        print(question)

if __name__ == '__main__':
    main()
