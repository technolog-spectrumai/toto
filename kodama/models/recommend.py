from django.db import models
from django.db import models


class RecommenderSettings(models.Model):
    weight_user = models.FloatField(default=1.0)
    weight_item = models.FloatField(default=1.0)
    weight_content = models.FloatField(default=1.0)
    cache_timeout = models.PositiveIntegerField(default=3600, help_text="Cache duration in seconds")
    cooldown_minutes = models.PositiveIntegerField(default=30, help_text="Minutes to exclude recently seen articles")
    top_similar_users = models.PositiveIntegerField(default=12)

    def __str__(self):
        return f"RecommenderSettings No. {self.pk}"


class RecommendationScores(models.Model):
    site = models.ForeignKey('SiteConfig', on_delete=models.CASCADE)
    user_item_matrix = models.JSONField()
    item_feature_matrix = models.JSONField()
    article_ids = models.JSONField(default=list)
    user_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"RecommendationScores for {self.site} (created: {self.created_at})"

    def save(self, *args, **kwargs):
        # Deactivate other scores for the same site if this one is set active
        if self.active:
            RecommendationScores.objects.filter(site=self.site, active=True).exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)