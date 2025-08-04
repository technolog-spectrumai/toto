from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.models import User
from kodama.models import (
    Article,
    AuthorProfile,
    Category,
    Tag,
    SiteConfig,
    Section
)

class Command(BaseCommand):
    help = "Seeds Technology category and sample articles with sections for a given site."

    def add_arguments(self, parser):
        parser.add_argument("site_name", type=str, help="Site title to associate new content with")

    def handle(self, *args, **options):
        site = self.get_site(options["site_name"])
        if not site:
            return

        author_profile = self.get_author_profile("janek")
        category = self.get_or_create_category(site)
        tags = self.get_or_create_tags(site)

        for i, keyword in enumerate(["apple", "banana", "kiwi", "mango", "orange", "plum"]):
            title, abstract, selected_tags = self.generate_article_meta(i, keyword, tags)
            article = self.create_article(title, abstract, site, author_profile)

            if not article:
                continue

            article.categories.add(category)
            article.tags.add(*selected_tags)

            self.create_sections(article, i)

        self.stdout.write(self.style.SUCCESS("🚀 Sample articles and sections populated."))

    def get_site(self, site_name):
        slug = slugify(site_name)
        try:
            return SiteConfig.objects.get(slug=slug)
        except SiteConfig.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ SiteConfig with slug '{slug}' not found."))
            return None

    def get_author_profile(self, username):
        user, _ = User.objects.get_or_create(username=username)
        profile, _ = AuthorProfile.objects.get_or_create(
            user=user,
            defaults={"bio": "Tech enthusiast."}
        )
        return profile

    def get_or_create_category(self, site):
        return Category.objects.get_or_create(name="Technology", slug="technology", site=site)[0]

    def get_or_create_tags(self, site):
        tag_defs = {
            "ai": "AI",
            "quantum": "Quantum Computing",
            "tech": "Technology"
        }
        return {
            key: Tag.objects.get_or_create(name=name, slug=slugify(name), site=site)[0]
            for key, name in tag_defs.items()
        }

    def generate_article_meta(self, i, suffix, tags):
        if i % 2 == 0:
            return (
                f"AI Advancements in 2025 - {suffix}",
                "The AI boom continues",
                [tags["ai"], tags["tech"]]
            )
        else:
            return (
                f"The Future of Quantum Computing - {suffix}",
                "Quantum computing takes a leap forward",
                [tags["quantum"], tags["tech"]]
            )

    def create_article(self, title, abstract, site, author_profile):
        slug = slugify(title)
        article, created = Article.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "abstract": abstract,
                "site": site,
                "author": author_profile,
                "version": "v1",
                "is_draft": False,
            }
        )
        if not created:
            self.stdout.write(f"📝 Article '{slug}' already exists. Skipping.")
            return None
        return article

    def create_sections(self, article, index):
        lorem = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
        )
        for part in [1, 2]:
            Section.objects.create(
                article=article,
                order=part,
                title=self.get_section_title(index, part),
                content=lorem * 3,
            )
        self.stdout.write(f"📚 Sections added to '{article.title}'")

    def get_section_title(self, index, part):
        if index % 2 == 0:
            return "Intro to AI" if part == 1 else "Impacts on Daily Life"
        else:
            return "Quantum Breakthroughs" if part == 1 else "Challenges Ahead"
