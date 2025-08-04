import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderBase:
    @staticmethod
    def merge_real_and_predicted_ratings(user_index, user_item_matrix, predicted_ratings):
        merged_ratings = {}
        num_items = user_item_matrix.shape[1]

        for item_index in range(num_items):
            real_rating = user_item_matrix[user_index, item_index]
            if real_rating > 0:
                merged_ratings[item_index] = float(real_rating)
            elif item_index in predicted_ratings:
                merged_ratings[item_index] = float(round(predicted_ratings[item_index], 4))
            else:
                merged_ratings[item_index] = 0

        return merged_ratings

    @staticmethod
    def choose_best_n(rating_dict, top_n=3):
        sorted_items = sorted(
            [(item, float(rating)) for item, rating in rating_dict.items() if rating is not None],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_items[:top_n]










