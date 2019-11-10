""" Object containing information from a Question Summary """


class QuestionSummary():
    html_tag = "div"
    summary = "question-summary"

    def __init__(self):
        self.ref = None
        self.vote_count = None
        self.answer_count = None
        self.view_count = None
        self.question = None
        self.tags = None
        self.date = None

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

    def __str__(self):
        return str(self.__dict__)

    def get_dict_of_attributes(self):
        return self.__dict__
