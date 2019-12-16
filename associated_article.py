"""Stores association between Question Summary Id and Tag Id"""
from generic_observation import GenericObservation


class AssociatedArticle(GenericObservation):

    def __init__(self, article_id, qs_id):
        self.article_id = article_id
        self.question_summary_id = qs_id
