""" Article class contains the fields of a Article object"""
from generic_observation import GenericObservation
import re


class Article(GenericObservation):
    def __init__(self, args):
        self.abstract = args.get('abstract', "").strip()[:500]
        self.web_url = args.get('web_url', "").strip()[:150]
        self.snippet = args.get('snippet', "").strip()[:500]
        self.lead_paragraph = args.get('lead_paragraph', "").strip()[:500]
        self.print_section = args.get('print_section', "").strip()[:45]
        self.print_page = args.get('print_page', "").strip()[:45]
        self.source_name = args.get('source', "").strip()[:45]
        self.headline = args.get('headline', {}).get('main', "").strip()[:45]
        self.pub_date = args.get('pub_date', "").strip()[:-5]
        self.document_type = args.get('document_type', "").strip()[:45]
        self.section_name = args.get('section_name', "").strip()[:45]
        self.id = args.get('_id', "").strip()[:150]
        self.replace_double_quotes()

    def replace_double_quotes(self):
        """
        Replaces double quotes with single quotes for all attributes of self
        """
        for key in self.__dict__.keys():
            string = getattr(self, key)
            clean_string = re.sub('\"', "'", string)
            setattr(self, key, clean_string)

    def get_attributes(self):
        return self.__dict__
