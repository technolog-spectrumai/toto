from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone


class ArticleFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    liked = models.BooleanField()  # True = like, False = dislike
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "article")  # Each user can vote once

    def __str__(self):
        sentiment = "liked" if self.liked else "disliked"
        return f"{self.user.username} {sentiment} '{self.article.title}'"


class Hit(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="hits")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    @staticmethod
    def log_if_allowed(request, article, cooldown_minutes=5):
        cutoff = timezone.now() - timedelta(minutes=cooldown_minutes)
        user = request.user if request.user.is_authenticated else None
        ip = request.META.get("REMOTE_ADDR")

        filters = {
            "article": article,
            "timestamp__gte": cutoff,
            "user": user if user else None,
        }

        if not user:
            filters["ip_address"] = ip

        if not Hit.objects.filter(**filters).exists():
            Hit.objects.create(
                article=article,
                user=user,
                ip_address=ip,
                user_agent=request.META.get("HTTP_USER_AGENT", "")
            )

    @staticmethod
    def get_recently_seen_articles(user, cooldown_minutes=30):
        cutoff = timezone.now() - timedelta(minutes=cooldown_minutes)

        filters = {"timestamp__gte": cutoff}
        if user and user.is_authenticated:
            filters["user"] = user

        return list(Hit.objects.filter(**filters).values_list("article_id", flat=True))