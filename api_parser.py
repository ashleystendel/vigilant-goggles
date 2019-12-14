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
        # TODO: error handling on get request
        request_string = self.base_url + '\{' + key_words + '}&api-key=' + self.key
        response = requests.get(request_string)
        info = response.json()
        obj = klass(info)
        return obj

    def get_responses(self, klass, reference_objects):
        """
        returns list of objects of type klass
        :param klass: type of object
        :param num_pages: number of pages to parse (default 1)
        :return: list of populated objects of type klass
        """
        responses = []
        for obj in reference_objects:
            key_words = obj.get_tags()
            responses.append(self.get_response(key_words, klass))

        return responses
