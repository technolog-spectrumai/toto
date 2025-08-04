from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from kodama.models import SiteConfig, AuthorProfile, Article, Tag, Category, Source, Font, Theme
from datetime import date


User = get_user_model()


class SmokeTestURLs(TestCase):

    def setUp(self):
        # Create test user and login
        self.user = User.objects.create_user("tester", "t@t.com", "pass")
        self.client = Client()
        self.client.login(username="tester", password="pass")

        # Create font and theme
        self.font = Font.objects.create(
            name="Playfair Display",
            cdn_link="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap"
        )
        self.theme = Theme.objects.create(
            name="Default",
            theme=[],
            font=self.font
        )

        # Minimal site setup with theme
        self.site = SiteConfig.objects.create(
            site_title="Smoke",
            slug="smoke",
            current_year=2025,
            contact_email="x@x.x",
            contact_phone="000",
            author="tester",
            about_page_content="About",
            theme=self.theme
        )

        # Minimal related objects
        self.profile = AuthorProfile.objects.create(user=self.user)
        self.cat = Category.objects.create(name="C", slug="c", site=self.site)
        self.tag = Tag.objects.create(name="T", slug="t", site=self.site)
        self.source = Source.objects.create(
            title="S",
            type="book",
            creator="c",
            publication_date=date(2021, 5, 17),
        )
        self.article = Article.objects.create(
            title="A", slug="a", abstract="y",
            author=self.profile, site=self.site
        )
        self.article.categories.add(self.cat)
        self.article.tags.add(self.tag)
        self.article.sources.add(self.source)

    def test_all_urls(self):
        routes = [
            ("site_home",       ["smoke"], {}),
            ("article_detail",  ["smoke", "a"], {}),
            ("article_feedback",["smoke", "a"], {"post": {"liked": "true"}}),
            ("contact",         ["smoke"], {"post": {"name": "X", "email": "x@x.x", "message": "hi"}}),
            ("about",           ["smoke"], {}),
            ("articles_by_category", ["smoke", "c"], {}),
            ("articles_by_tag",     ["smoke", "t"], {}),
            ("latest_articles",      ["smoke"], {}),
            ("article_search",       ["smoke"], {}),
            ("source_detail", ["smoke", self.source.pk], {}),
            ("source_list",   ["smoke"], {}),
            ("author_profile",["smoke", self.user.username], {}),
            ("profile_detail",["smoke", self.user.username], {}),
            ("kodama_logout", ["smoke"], {}),
            ("kodama_login",  ["smoke"], {"post": {"username": "tester", "password": "pass"}}),
            ("goodbye",       ["smoke"], {}),
        ]

        for name, args, ops in routes:
            try:
                url = reverse(name, args=args)
            except NoReverseMatch:
                self.fail(f"Could not reverse {name} with args {args}")

            # GET always
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 500, f"{name} GET failed")

            # POST if provided
            if "post" in ops:
                response = self.client.post(url, ops["post"])
                self.assertNotEqual(response.status_code, 500, f"{name} POST failed")
