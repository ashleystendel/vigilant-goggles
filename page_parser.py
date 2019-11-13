""" Module that fetches information from website """
import time

import requests
import re
from bs4 import BeautifulSoup
import question_summary


class PageParser:

    def __init__(self, url):
        self.url = url
        self.website = None
        self.soup = None

    def get_webpage(self, i):
        self.website = requests.get(self.url+i)

    def boil_soup(self):
        self.soup = BeautifulSoup(self.website.text, 'html.parser')

    def get_and_boil_soup(self, i):
        self.get_webpage(i)
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

    def get_page(self, klass, i):
        self.get_and_boil_soup(i)
        summary_page = []
        matches = self.get_matches(klass.HTML_TAG, klass.KEYWORD)

        for match in matches:
            item = klass(self)
            item.scrape_info(match)
            summary_page.append(item)

        return summary_page

    def get_pages(self, klass, num_pages=1):
        summaries = []
        for i in range(1, num_pages+1):
            summaries.extend(self.get_page(klass, str(i)))
        return summaries

