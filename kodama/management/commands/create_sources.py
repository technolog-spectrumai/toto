from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import date
from kodama.models import Source


class Command(BaseCommand):
    help = "Creates a set of sample book sources."

    def handle(self, *args, **options):
        # A small collection of invented books
        sample_books = [
            {
                "title": "The Pragmatic Programmer: Journeyman to Master",
                "creator": "Andrew Hunt & David Thomas",
                "publication_date": date(1999, 10, 30),
                "url": "https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/"
            },
            {
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "creator": "Robert C. Martin",
                "publication_date": date(2008, 8, 1),
                "url": "https://www.oreilly.com/library/view/clean-code/9780136083238/"
            },
            {
                "title": "You Don't Know JS: Scope & Closures",
                "creator": "Kyle Simpson",
                "publication_date": date(2014, 3, 23),
                "url": "https://github.com/getify/You-Dont-Know-JS"
            },
            {
                "title": "Deep Learning with Python",
                "creator": "Francois Chollet",
                "publication_date": date(2017, 10, 28),
                "url": "https://www.manning.com/books/deep-learning-with-python"
            },
            {
                "title": "Introduction to Algorithms",
                "creator": "Thomas H. Cormen, et al.",
                "publication_date": date(2009, 7, 31),
                "url": "https://mitpress.mit.edu/9780262033848/introduction-to-algorithms-third-edition/"
            },
        ]

        for info in sample_books:
            # We'll derive a slug for the title if you ever add slug support
            # slug = slugify(info["title"])

            source, created = Source.objects.get_or_create(
                title=info["title"],
                defaults={
                    "creator": info["creator"],
                    "publication_date": info["publication_date"],
                    "type": "book",
                    "url": info["url"],
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created Source: {source.title!r}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Source already exists: {source.title!r}")
                )

        self.stdout.write(self.style.SUCCESS("Sample book sources populated."))
