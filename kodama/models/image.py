from django.db import models
from django.db import models


class ArticleImage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    file = models.ImageField(upload_to="section_images/")
    source = models.ForeignKey("Source", on_delete=models.SET_NULL, null=True, blank=True, related_name="images")

    def __str__(self):
        return self.title

    @property
    def name(self):
        return f"{self.title} from '{self.source}'"
