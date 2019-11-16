""" Tag class contains the fields of a tag object"""
import re


class Tag:
    
    HTML_TAG = "div"
    KEYWORD = "tag-cell"

    def __init__(self, parser=None):
        self.name = ""
        self.count_day = None
        self.count_week = None
        self.count_month = None
        self.count_year = None
        self.total_count = None
        self.parser = parser

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
        :return: None
        """
        if "today" in count:
            self.count_day = self.extract_count(count)
        elif "week" in count: 
            self.count_week = self.extract_count(count)
        elif "month" in count:
            self.count_month = self.extract_count(count)
        elif "year" in count:
            self.count_year = self.extract_count(count)

    def set_counts(self, counts):
        """
        sets the calendar count attributes based on lists of sentences
        :param counts: List of sentences containing tag count per day/week/month/year
        :return: None
        """
        for c in counts[0].split(','):
            self.set_count(c)
