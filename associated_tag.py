"""Stores association between Question Summary Id and Tag Id"""
from generic_observation import GenericObservation


class AssociatedTag(GenericObservation):

    def __init__(self, tag_id, qs_id):
        self.tag_id = tag_id
        self.question_summary_id = qs_id
