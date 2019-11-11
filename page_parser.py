""" Module that fetches information from website """
import requests
import re
from question_summary import *
from user import *
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class PageParser:

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

    def get_matches(self, html_tag, keyword, item=None):
        item = self.soup if item is None else item
        return item.find_all(html_tag, class_=keyword)

    def get_match_text(self, html_tag, keyword, tag):
        return self.get_matches(html_tag, keyword, tag)[0].get_text()

    def get_match_int(self, html_tag, keyword, tag):
        tmp = self.get_match_text(html_tag, keyword, tag)
        return int(re.findall(r'\d+', tmp)[0])

    def get_match_other(self, html_tag, keyword, tag, other):
        return self.get_matches(html_tag, keyword, tag)[0][other]

    def get_match_tags(self, html_tag, keyword, tag):
        return [x.get_text() for x in self.get_matches(html_tag, keyword, tag)]
