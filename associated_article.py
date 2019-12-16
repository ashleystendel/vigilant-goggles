"""Stores association between Question Summary Id and Tag Id"""


class AssociatedArticle:

    def __init__(self, article_id, qs_id):
        self.article_id = article_id
        self.question_summary_id = qs_id

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