from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forum.models import Topic, Post

class Command(BaseCommand):
    help = "Prepopulate the database with sample topics and posts."

    def handle(self, *args, **kwargs):
        # Create a test user
        user, created = User.objects.get_or_create(username="testuser", defaults={"email": "test@example.com"})
        if created:
            user.set_password("password123")
            user.save()

        # Create sample topics
        topics = [
            {"title": "Welcome to the Forum", "description": "Introduce yourself and get started."},
            {"title": "Django Tips & Tricks", "description": "Share useful Django insights."},
            {"title": "General Discussions", "description": "Talk about anything tech-related!"},
        ]

        for topic_data in topics:
            topic, _ = Topic.objects.get_or_create(**topic_data)
            Post.objects.create(topic=topic, author=user, content="This is a sample post in this topic.")

        self.stdout.write(self.style.SUCCESS("Successfully prepopulated the database!"))
