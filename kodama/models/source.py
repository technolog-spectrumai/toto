from django.db import models
from django.db import models



class Source(models.Model):
    SOURCE_TYPES = [
        ('book', 'Book'),
        ('music', 'Music'),
        ('video', 'Video'),
        ('article', 'Article'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    creator = models.CharField(max_length=100, blank=True)  # e.g., author, director
    publication_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=SOURCE_TYPES)
    url = models.URLField(blank=True)  # optional: link to the source

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    @property
    def name(self):
        return f"{self.title} by {self.creator} ({self.get_type_display()})"