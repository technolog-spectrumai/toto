from django.db import models
from django.db import models



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


