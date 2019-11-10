""" Author: Jacob Mooney and Ashley Stendel 
    This program scrapes https://medicalsciences.stackexchange.com/ """
from page_parser import *


def main():
    parser = PageParser("https://medicalsciences.stackexchange.com/")
    print(parser.get_question_summaries())


if __name__ == '__main__':
    main()
