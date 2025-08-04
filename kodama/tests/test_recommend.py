import numpy as np
from django.test import TestCase
from django.contrib.auth import get_user_model

from kodama.models import Article, ArticleFeedback, AuthorProfile, SiteConfig
from kodama.recommend import RecommendationEngine

User = get_user_model()


class RecommendationEngineTest(TestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username="alice", password="pass")
        self.user2 = User.objects.create_user(username="bob", password="pass")

        # AuthorProfile & SiteConfig
        self.author_profile = AuthorProfile.objects.create(
            user=self.user1,
            bio="Author Alice"
        )
        self.site = SiteConfig.objects.create(
            site_title="Test Site",
            slug="test-site",
            current_year=2025,
            contact_email="contact@example.com",
            contact_phone="123456789",
            author="Admin",
            about_page_content="About..."
        )

        # Two Articles
        self.article1 = Article.objects.create(
            title="First Article",
            slug="first-article",
            abstract="Abstract A",
            author=self.author_profile,
            site=self.site
        )
        self.article2 = Article.objects.create(
            title="Second Article",
            slug="second-article",
            abstract="Abstract B",
            author=self.author_profile,
            site=self.site
        )

        # Feedback (+1 if liked else -1)
        ArticleFeedback.objects.create(user=self.user1, article=self.article1, liked=True)
        ArticleFeedback.objects.create(user=self.user2, article=self.article1, liked=False)
        ArticleFeedback.objects.create(user=self.user2, article=self.article2, liked=True)

    def test_build_user_item_matrix(self):
        # Fetch sorted ID lists
        user_ids = RecommendationEngine.get_user_ids()
        article_ids = RecommendationEngine.get_article_ids()

        # Build the matrix
        matrix = RecommendationEngine.build_user_item_matrix(user_ids, article_ids)
        self.assertIsInstance(matrix, np.ndarray)

        # Compute expected shape: (#users × #articles)
        self.assertEqual(matrix.shape, (len(user_ids), len(article_ids)))

        # Find indices in the sorted lists
        u1_i = user_ids.index(self.user1.id)
        u2_i = user_ids.index(self.user2.id)
        a1_i = article_ids.index(self.article1.id)
        a2_i = article_ids.index(self.article2.id)

        # Assert ratings:  +1, -1, +1
        self.assertEqual(matrix[u1_i, a1_i],  1)   # user1 liked article1
        self.assertEqual(matrix[u2_i, a1_i], -1)   # user2 disliked article1
        self.assertEqual(matrix[u2_i, a2_i],  1)   # user2 liked article2
