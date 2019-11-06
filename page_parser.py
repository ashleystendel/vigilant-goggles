""" Module that fetches information from website """
import requests
from bs4 import BeautifulSoup


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

    def get_information(self, html_tag, keyword):
        return self.soup.find_all(html_tag, class_=keyword)
