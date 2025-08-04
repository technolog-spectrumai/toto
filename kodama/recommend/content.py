import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .base import RecommenderBase


class RecommenderContent(RecommenderBase):

    @staticmethod
    def compute_content_similarity(item_feature_matrix):
        return cosine_similarity(item_feature_matrix)

    @staticmethod
    def predict_ratings_for_user(user_index, user_item_matrix, item_feature_matrix):
        user_ratings = user_item_matrix[user_index]
        item_similarity_matrix = cosine_similarity(item_feature_matrix)
        num_items = user_item_matrix.shape[1]
        predicted_ratings = {}

        for item_index in range(num_items):
            if user_ratings[item_index] == 0:
                numerator = 0.0
                denominator = 0.0
                for other_item_index in range(num_items):
                    rating = user_ratings[other_item_index]
                    if rating > 0:
                        sim = item_similarity_matrix[item_index, other_item_index]
                        numerator += sim * rating
                        denominator += abs(sim)
                if denominator > 0:
                    predicted_ratings[item_index] = numerator / denominator
        return predicted_ratings.items()