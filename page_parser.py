""" Parser object that fetches information from website """
import time

import requests
import re
from bs4 import BeautifulSoup


class PageParser:

    def __init__(self, url):
        self.url = url
        self.website = None
        self.soup = None

    def get_webpage(self, i):
        """
        performs get request to specific webpage and sets website attribute
        :param i: webpage number
        :return: None
        """
        self.website = requests.get(self.url+i)

    def boil_soup(self):
        """
        create and sets BeautifulSoup soup attribute from webpage for parsing
        :return: None
        """
        self.soup = BeautifulSoup(self.website.text, 'html.parser')

    def get_and_boil_soup(self, i):
        """
        performs a get request to website and create BeautifulSoup soup object from webpage for parsing
        :param i: webpage number
        :return:
        """
        self.get_webpage(i)
        self.boil_soup()

    def get_matches(self, html_tag, keyword, item=None):
        """
        returns a list of html snippets that contain the required information
        based on the html_tag and the name of the class
        :param html_tag: html tag
        :param keyword: name of the class in html tag
        :param item: None or html snippet
        :return: list of html snippets
        """
        item = self.soup if item is None else item
        return item.find_all(html_tag, class_=keyword)

    def get_match_text(self, html_tag, keyword, tag):
        """
        returns the string text from the html snippet
        :param html_tag: html tag
        :param keyword: name of the class in html tag
        :param tag: html snippet
        :return: string text from the html tag
        """
        return self.get_matches(html_tag, keyword, tag)[0].get_text()

    def get_match_int(self, html_tag, keyword, tag):
        """
        gets the integer content from the html snippet text
        :param html_tag: html tag
        :param keyword: name of the class in html tag
        :param tag: html snippet
        :return: integer content from the html tag
        """
        tmp = self.get_match_text(html_tag, keyword, tag)
        return int(re.findall(r'\d+', tmp)[0])

    def get_match_other(self, html_tag, keyword, tag, other):
        """
        returns the content from within a tag ex: <a href="get this content"/a>
        :param html_tag: html tag
        :param keyword: name of the class in html tag
        :param tag: html snippet
        :param other: tag containing information
        :return: content from within the html tag
        """
        return self.get_matches(html_tag, keyword, tag)[0][other]

    def get_match_list(self, html_tag, keyword, tag):
        """
        returns the string content from a list of repeating items
        :param html_tag: html tag
        :param keyword: name of the class in html tag
        :param tag: html snippet
        :return: list of string content
        """
        return [x.get_text() for x in self.get_matches(html_tag, keyword, tag)]

    def get_page(self, klass, i):
        """
        returns list of objects of type klass by extracting html content of one webpage
        :param klass: type of object
        :param i: page number
        :return: list of populated objects of type klass
        """
        self.get_and_boil_soup(i)
        summary_page = []
        matches = self.get_matches(klass.HTML_TAG, klass.KEYWORD)

        for match in matches:
            item = klass(self)
            item.scrape_info(match)
            summary_page.append(item)

        return summary_page

    def get_pages(self, klass, num_pages=1):
        """
        returns list of objects of type klass by extracting html content of >= 1 webpage(s)
        :param klass: type of object
        :param num_pages: number of pages to parse (default 1)
        :return: list of populated objects of type klass
        """
        summaries = []
        for i in range(1, num_pages+1):
            summaries.extend(self.get_page(klass, str(i)))
        return summaries

