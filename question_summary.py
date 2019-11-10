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
        print(f'{self.vote_count}, {self.vote_count}, {self.answer_count}, ' +
              f'{self.view_count}, {self.question}, {self.tags}, {self.date}')