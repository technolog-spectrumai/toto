from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="child_posts", null=True, blank=True)  # Self-referential FK
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    depth = models.PositiveIntegerField(default=0)  # Track nesting depth

    def save(self, *args, **kwargs):
        if self.parent:
            self.depth = self.parent.depth + 1  # Increase depth by 1 if it's a reply
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{'↳ ' * self.depth}Post by {self.author.username} in {self.topic.title}"
