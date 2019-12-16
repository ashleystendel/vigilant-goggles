""" API Parser that gets a list of objects from url specified in config"""
from config import api
import requests
from logger import Logger
import time

log = Logger()


class APIParser:

    def __init__(self):
        self.base_url = api['base_url']
        self.key = api['key']

    def get_response(self, key_words, klass):
        """
        performs get request to specific api
        :param i: list of key words
        """
        # TODO: error handling on get request
        request_string = self.base_url + '\{' + ",".join(key_words) + '}&api-key=' + self.key
        response = requests.get(request_string)
        time.sleep(6)
        if response.status_code == 200:
            info = response.json()
            obj_dict = info['response']['docs']
            obj_lst = [klass(a) for a in obj_dict]
            return obj_lst
        else:
            log.logger.error(f'Error during API - Call: {response.status_code} {response.content}')
        return []

    def get_responses(self, klass, reference_objects):
        """
        returns list of objects of type klass
        :param klass: type of object
        :param num_pages: number of pages to parse (default 1)
        :return: list of populated objects of type klass
        """
        responses = []
        for obj in reference_objects:
            key_words = [t.name for t in obj.tags]
            obj_lst = self.get_response(key_words, klass)
            responses.append(obj_lst)
        return responses
