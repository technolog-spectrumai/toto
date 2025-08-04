from django.db import models
from django.db import models


class GeneralPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ForeignKey(
        "ArticleImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_posts"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Section(GeneralPost):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="sections"
    )
    order = models.PositiveIntegerField(
        help_text="Order of this section within the article"
    )

    class Meta:
        ordering = ["order"]
        unique_together = ("article", "order")

    def __str__(self):
        return f"Section {self.order}: {self.title}"
