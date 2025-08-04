from django.db import models
from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags
import re



class Category(models.Model):
    site = models.ForeignKey('SiteConfig', on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        unique_together = ("site", "slug")  # Ensure uniqueness per site

    def __str__(self):
        return f"[{self.site}] {self.name}"


class Tag(models.Model):
    site = models.ForeignKey('SiteConfig', on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=64)
    slug = models.SlugField()

    class Meta:
        unique_together = ("site", "slug")  # Ensure uniqueness per site

    def __str__(self):
        return f"[{self.site}] {self.name}"


class GeneralArticle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey("SiteConfig", on_delete=models.CASCADE, related_name="articles")
    author = models.ForeignKey("AuthorProfile", on_delete=models.CASCADE, related_name="articles", blank=True, null=True)
    categories = models.ManyToManyField("Category", related_name="articles")
    tags = models.ManyToManyField("Tag", related_name="articles", blank=True)
    version = models.CharField(max_length=16, default="v1")
    is_draft = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Article(GeneralArticle):
    abstract = models.TextField()
    sources = models.ManyToManyField("Source", related_name="articles", blank=True)
    image = models.ForeignKey("ArticleImage", on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")

    @property
    def word_count(self):
        total_words = 0
        for section in self.sections.all():
            text = strip_tags(section.content or "")
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            total_words += len(cleaned_text.split())
        return total_words

    def __str__(self):
        return f"Article {self.title} by {self.author}"


