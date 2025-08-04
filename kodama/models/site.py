from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django_jsonform.models.fields import JSONField
from django.utils.text import slugify


SOCIAL_LINK_SCHEMA = {
    "type": "array",
    "title": "Social Links",
    "items": {
        "type": "object",
        "title": "Social Media",
        "properties": {
            "name": {
                "type": "string",
                "title": "Platform Name",
                "description": "Name of the social media platform (e.g., Facebook, Twitter)"
            },
            "url": {
                "type": "string",
                "format": "uri",
                "title": "Profile URL",
                "description": "URL to the social media profile or platform"
            },
            "icon_class": {
                "type": "string",
                "title": "Icon Class",
                "description": "CSS class for the social media platform's icon"
            }
        },
        "required": ["name", "url", "icon_class"]
    }
}

class SiteConfig(models.Model):
    site_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    current_year = models.PositiveIntegerField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    author = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    social_links = JSONField(schema=SOCIAL_LINK_SCHEMA, default=[])
    about_page_content = models.TextField()
    enable_wysiwyg = models.BooleanField(default=True)
    num_recommendations = models.PositiveIntegerField(default=4)
    num_latest = models.PositiveIntegerField(default=10)
    cache_lifetime = models.PositiveIntegerField(default=3600, help_text="Cache duration in seconds")
    measure_read_time = models.BooleanField(
        default=True,
        help_text="Enable reading time tracking for users"
    )

    recommender_settings = models.ForeignKey(
        'RecommenderSettings',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_configs"
    )

    theme = models.ForeignKey(
        'Theme',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_configs",
        help_text="Style theme associated with this site"
    )

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.site_title)
        super().save(*args, **kwargs)