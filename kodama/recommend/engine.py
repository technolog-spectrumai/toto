import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from kodama.models import Article, ArticleFeedback, RecommendationScores, RecommenderSettings, Hit
from kodama.recommend import RecommenderUser, RecommenderItem, RecommenderContent
from django.core.cache import cache
from django.contrib.auth import get_user_model


class RecommendationEngine:

    def __init__(self, weight_user=1.0, weight_item=1.0, weight_content=1.0, cache_timeout=3600):
        self.weight_user = weight_user
        self.weight_item = weight_item
        self.weight_content = weight_content
        self.cache_timeout = cache_timeout

    @staticmethod
    def create(settings: RecommenderSettings):
        return RecommendationEngine(
            weight_user=settings.weight_user,
            weight_item=settings.weight_item,
            weight_content=settings.weight_content,
            cache_timeout=settings.cache_timeout
        )

    @staticmethod
    def get_user_ids():
        User = get_user_model()
        all_users = list(User.objects.all().values_list("id", flat=True))
        return sorted(all_users)

    @staticmethod
    def get_article_ids():
        all_articles = list(Article.objects.all().values_list("id", flat=True))
        return sorted(all_articles)

    @staticmethod
    def build_user_item_matrix(user_ids, item_ids):
        feedback = ArticleFeedback.objects.values("user_id", "article_id", "liked")

        user_index = {uid: idx for idx, uid in enumerate(user_ids)}
        item_index = {aid: idx for idx, aid in enumerate(item_ids)}

        matrix = np.zeros((len(user_ids), len(item_ids)))
        for row in feedback:
            uid = row["user_id"]
            aid = row["article_id"]
            rating = 1 if row["liked"] else -1
            matrix[user_index[uid], item_index[aid]] = rating

        return matrix

    @staticmethod
    def build_item_feature_matrix():
        article_tag_map = {
            article.id: [tag.name for tag in article.tags.all()]
            for article in Article.objects.prefetch_related("tags")
        }

        article_ids = list(article_tag_map.keys())
        tag_lists = [article_tag_map[aid] for aid in article_ids]

        mlb = MultiLabelBinarizer()
        matrix = mlb.fit_transform(tag_lists)
        return matrix

    @staticmethod
    def _normalize_scores(scored_items):
        if not scored_items:
            return []
        scores = [score for score, _ in scored_items]
        min_score, max_score = min(scores), max(scores)
        if max_score == min_score:
            return [(1.0, aid) for _, aid in scored_items]
        return [(aid, float((score - min_score) / (max_score - min_score))) for aid, score in scored_items]

    def get_weighted_recommendations(self, user_index, user_item_matrix, item_feature_matrix, top_similar_users=12):
        score_total = {}

        # User-Based
        sim_user = RecommenderUser.compute_similarity(user_item_matrix)
        top_users = RecommenderUser.find_top_n_similar_users_by_index(user_index, sim_user, top_similar_users)
        user_scores = RecommenderUser.predict_ratings_from_similar_users(user_index, user_item_matrix, top_users)
        norm_user = self._normalize_scores(user_scores)
        for aid, score in norm_user:
            score_total[aid] = score_total.get(aid, 0) + score * self.weight_user

        # Item-Based
        sim_item = RecommenderItem.compute_item_similarity(user_item_matrix)
        item_scores = RecommenderItem.predict_ratings_for_user(user_index, user_item_matrix, sim_item)
        norm_item = self._normalize_scores(item_scores)
        for aid, score in norm_item:
            score_total[aid] = score_total.get(aid, 0) + score * self.weight_item

        # Content-Based
        content_scores = RecommenderContent.predict_ratings_for_user(user_index, user_item_matrix, item_feature_matrix)
        norm_content = self._normalize_scores(content_scores)
        for aid, score in norm_content:
            score_total[aid] = score_total.get(aid, 0) + score * self.weight_content

        final_sorted = sorted(score_total.items(), key=lambda x: x[1], reverse=True)
        return [(int(i[0]), float(i[1])) for i in final_sorted]

    def build(self, site):
        article_ids = self.get_article_ids()
        user_ids = self.get_user_ids()
        user_item_matrix = self.build_user_item_matrix(user_ids, article_ids)
        item_feature_matrix = self.build_item_feature_matrix()

        return RecommendationScores.objects.create(
            site=site,
            user_item_matrix=user_item_matrix.tolist(),
            item_feature_matrix=item_feature_matrix.tolist(),
            article_ids=article_ids,
            user_ids = user_ids
        )

    @staticmethod
    def remap(scored_items, article_ids):
        results = []
        for matrix_index, score in scored_items:
            try:
                article_id = article_ids[matrix_index]
                article = Article.objects.get(id=article_id)
                results.append((article, score))
            except (IndexError, Article.DoesNotExist):
                continue
        return results

    def predict(self, site, user, include_list = None):
        score = RecommendationScores.objects.filter(site=site, active=True).order_by("-created_at").first()
        if score is None:
            return []
        settings = site.recommender_settings
        user_index = score.user_ids.index(user.id)
        raw_scores = self.get_weighted_recommendations(
            user_index=user_index,
            user_item_matrix=np.array(score.user_item_matrix),
            item_feature_matrix=np.array(score.item_feature_matrix),
            top_similar_users=settings.top_similar_users
        )
        article_score_pairs = self.remap(raw_scores, score.article_ids)
        seen_ids = Hit.get_recently_seen_articles(user, cooldown_minutes=settings.cooldown_minutes)
        if include_list is None:
            filtered_pairs = [
                (article, score_val)
                for article, score_val in article_score_pairs
                if article.id not in seen_ids
            ]
        else:
            filtered_pairs = [
                (article, score_val)
                for article, score_val in article_score_pairs
                if article.id in include_list and article.id not in seen_ids
            ]
        top_n = site.num_recommendations
        return [article for article, score in filtered_pairs][:top_n]


