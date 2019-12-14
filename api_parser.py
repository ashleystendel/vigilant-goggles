""" API Parser that """

from config import api
import requests


class APIParser:

    def __init__(self):
        self.base_api = api.base_url
        self.key = api.key

    def get_response(self, key_words, klass):
        """
        performs get request to specific api
        :param i: list of key words
        """
        # TODO: make the request string more agnostic
        request_string = self.base_url + '\{' + key_words + '}&api-key=' + self.key
        info = requests.get(request_string)
        obj = klass(info)
        return obj

    def get_responses(self, klass):
        """
        returns list of objects of type klass
        :param klass: type of object
        :param num_pages: number of pages to parse (default 1)
        :return: list of populated objects of type klass
        """
        responses = []
        data = [['blood', 'death'], 'hair']
        for datum in data:
            responses.extend(self.get_response(datum, klass))
        return responses
