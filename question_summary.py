""" Object containing information from a Question self """


class QuestionSummary:

    def __init__(self, parser):
        self.ref = None
        self.vote_count = None
        self.answer_count = None
        self.view_count = None
        self.question = None
        self.tags = None
        self.date = None
        self.parser = parser

    def pretty_print(self):
        info = (
                f'Question Text: {self.question}\n'
                f'Votes: {self.vote_count}\n'
                f'Answers: {self.answer_count}\n'
                f'Views: {self.view_count}\n'
                f'Tags: {self.tags}\n'
                f'Date Posted: {self.date}\n'
                f'URL: {self.ref}\n'
                )
        print(info)

    def scrape_info(self, input):
        self.ref = self.parser.get_match_other("a", "question-hyperlink", input, 'href')
        self.vote_count = self.parser.get_match_int("div", "votes", input)
        self.answer_count = self.parser.get_match_int("div", "status", input)
        self.view_count = self.parser.get_match_int("div", "views", input)
        self.question = self.parser.get_match_text("a", "question-hyperlink", input)
        self.tags = self.parser.get_match_tags("a", "post-tag", input)
        self.date = self.parser.get_match_other("span", "relativetime", input, 'title')

    def __str__(self):
        return str(self.__dict__)

    def get_attributes(self):
        return self.__dict__
