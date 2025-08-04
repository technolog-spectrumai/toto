import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .base import RecommenderBase


class RecommenderUser(RecommenderBase):

    @staticmethod
    def compute_similarity(user_item_matrix):
        return cosine_similarity(user_item_matrix)

    @staticmethod
    def find_top_n_similar_users_by_index(user_index, similarity_matrix, top_n=3):
        similarities = similarity_matrix[user_index]
        similarities_excl_self = similarities.copy()
        similarities_excl_self[user_index] = -1  # Exclude self
        top_indices = np.argsort(similarities_excl_self)[::-1][:top_n]
        return [(int(i), float(similarities[i])) for i in top_indices]

    @staticmethod
    def predict_ratings_from_similar_users(user_index, user_item_matrix, top_users):
        num_items = user_item_matrix.shape[1]
        predicted_ratings = []

        # Unpack indices and similarities
        similar_user_indices, similarities = zip(*top_users)
        similarities = np.array(similarities)

        if np.sum(similarities) == 0:
            # Default to user's own ratings
            predicted_ratings = [(item, user_item_matrix[user_index, item]) for item in range(num_items)]
            return predicted_ratings

        # Predict each item's rating
        for item in range(num_items):
            numerator = 0.0
            denominator = 0.0
            for sim_user_idx, sim in top_users:
                rating = user_item_matrix[sim_user_idx, item]
                if rating > 0:
                    numerator += sim * rating
                    denominator += sim
            predicted_score = numerator / denominator if denominator > 0 else 0.0
            predicted_ratings.append((item, predicted_score))
        return predicted_ratings