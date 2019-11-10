""" Module that fetches information from website """
import requests
import re
from question_summary import *
from bs4 import BeautifulSoup


def _get_match_int(html_tag, keyword, tag):
    tmp = tag.find(html_tag, class_=keyword)
    return int(re.findall(r'\d+', tmp.get_text())[0])


class PageParser():

    def __init__(self, url):
        self.url = url
        self.website = None
        self.soup = None
        self.get_and_boil_soup()

    def get_webpage(self):
        self.website = requests.get(self.url)

    def boil_soup(self):
        self.soup = BeautifulSoup(self.website.text, 'html.parser')

    def get_and_boil_soup(self):
        self.get_webpage()
        self.boil_soup()

    def get_matches(self, html_tag, keyword):
        return self.soup.find_all(html_tag, class_=keyword)

    def get_match_text(self, html_tag, keyword, tag):
        return tag.find(html_tag, class_=keyword).get_text()

    def get_match_int(self, html_tag, keyword, tag):
        tmp = tag.find(html_tag, class_=keyword).get_text()
        return int(re.findall(r'\d+', tmp)[0])

    def get_match_other(self, html_tag, keyword, tag, other):
        return tag.find(html_tag, class_=keyword)[other]

    def get_match_tags(self, html_tag, keyword, tag):
        return [x.get_text() for x in tag.find_all(html_tag, class_=keyword)]

    def get_question_summaries(self):

        summaries = []
        qs = self.get_matches(QuestionSummary.html_tag, QuestionSummary.summary)
        for q in qs:
            summary = QuestionSummary()
            summary.ref = self.get_match_other("a", "question-hyperlink", q, 'href')
            summary.vote_count = self.get_match_int("div", "votes", q)
            summary.answer_count = self.get_match_int("div", "status", q)
            summary.view_count = self.get_match_int("div", "views", q)
            summary.question = self.get_match_text("a", "question-hyperlink", q)
            summary.tags = self.get_match_tags("a", "post-tag", q)
            summary.date = self.get_match_other("span", "relativetime", q, 'title')
            summaries.append(summary)

        return summaries


