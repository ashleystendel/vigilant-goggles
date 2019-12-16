""" Tag class contains the fields of a tag object"""
import re


class Tag:
    
    HTML_TAG = "div"
    KEYWORD = "tag-cell"

    def __init__(self, parser=None, name=""):
        self.name = name
        self.count_day = 0
        self.count_week = 0
        self.count_month = 0
        self.count_year = 0
        self.total_count = 0
        self.parser = parser

    def convert_to_tuple(self, delete=[]):
        """
        gets values from object
        :param delete: list of attributes that are not needed not needed (ex: for sql select)
        :return: tuple of values for attributes
        """
        d_dict = self.__dict__.copy()
        for e in delete + ['parser']:
            d_dict.pop(e, None)
        return tuple(d_dict.values())

    def scrape_info(self, match):
        """
        sets the fields of a Tag from the html snippet
        :param match: html segment containing question summary
        """
        self.name = self.parser.get_match_text("a", "post-tag", match)
        counts = self.parser.get_match_list("div", 'stats-row', match)
        self.set_counts(counts)
        self.total_count = self.parser.get_match_int("span", "item-multiplier-count", match)

    def extract_count(self, count):
        """
        returns the integer count tag count within a sentence (ex: 11 asks this month)
        :param count: sentence containing tag count per day/week/month/year
        :return: integer tag count
        """
        return int(re.findall(r'\d+', count)[0])

    def set_count(self, count):
        """
        sets the calendar tag count attribute based on sentence
        (ex: 11 asks this month -> count_month = 11)
        :param count: sentence containing tag count per day/week/month/year
        """
        if "today" in count:
            self.count_day = int(self.extract_count(count))
        elif "week" in count: 
            self.count_week = int(self.extract_count(count))
        elif "month" in count:
            self.count_month = int(self.extract_count(count))
        elif "year" in count:
            self.count_year = int(self.extract_count(count))

    def set_counts(self, counts):
        """
        sets the calendar count attributes based on lists of sentences
        :param counts: List of sentences containing tag count per day/week/month/year
        """
        for c in counts[0].split(','):
            self.set_count(c)
