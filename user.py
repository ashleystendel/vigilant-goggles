from page_parser import *


class User:

    def __init__(self):
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

    def pretty_print(self):
        print(get_attributes())

    def scrape_info(self, input):
        return

    def get_attributes(self):
        return self.__dict__

    def set_username(self, username):
        self.username = username
