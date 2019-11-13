from page_parser import *


class User:

    def __init__(self, parser):
        self.reputation = None
        self.communities = []
        self.username = None
        self.answers = None
        self.questions = None
        self.people_reached = None
        self.membership_length = None
        self.profile_views = None
        self.last_login = None
        self.tags = []
        self.top_tag_score = {}
        self.parser = parser

    def pretty_print(self):
        print(get_attributes())

    def scrape_info(self, input):
        self.ref = self.parser.get_match_other("a", "question-hyperlink", input, 'href')
        self.vote_count = self.parser.get_match_int("div", "votes", input)
        self.answer_count = self.parser.get_match_int("div", "status", input)
        self.view_count = self.parser.get_match_int("div", "views", input)
        self.question = self.parser.get_match_text("a", "question-hyperlink", input)
        self.tags = self.parser.get_match_tags("a", "post-tag", input)
        self.date = self.parser.get_match_other("span", "relativetime", input, 'title')
        return

    def get_attributes(self):
        return self.__dict__

    def set_username(self, username):
        self.username = username
