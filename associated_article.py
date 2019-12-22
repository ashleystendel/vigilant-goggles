"""Stores association between Question Summary Id and Tag Id"""
from generic_observation import GenericObservation
import config
import requests


class AssociatedArticle(GenericObservation):

    def __init__(self, article_id, qs_id, article, qs):
        self.article_id = article_id
        self.question_summary_id = qs_id
        self.score = self.similarity_score_score(article, qs)

    def similarity_score_score(self, article, qs):
        """
        gets the similarity score between article and question
        using the paralleldots API
        :param article: Article object
        :param qs: QuestionSummary object
        :return: similarity score between aritcle and question
        """
        similarity_config = config.similarity
        data = {"text_1":  article.abstract,
                "text_2":  qs.question,
                "api_key": similarity_config['api_key']}

        response = requests.post(similarity_config['url'], data)
        score = response.json()['similarity_score']
        return score
