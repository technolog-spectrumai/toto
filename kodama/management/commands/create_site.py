from django.core.management.base import BaseCommand
from django.utils.text import slugify
from kodama.models import SiteConfig, Tag, RecommenderSettings, Theme


class Command(BaseCommand):
    help = "Creates a new SiteConfig with default tags, about content, and recommender settings."

    def add_arguments(self, parser):
        parser.add_argument("site_name", type=str, help="Name of the site to configure")
        parser.add_argument("theme", type=str, help="Name of the theme")

    def handle(self, *args, **options):
        site_title = options["site_name"]
        slug = slugify(site_title)
        current_year = 2025
        contact_email = "contact@kodama.com"
        contact_phone = "+48 123 456 789"
        author = "Jan Kowalski"

        social_links = [
            {"name": "Facebook", "url": "https://facebook.com", "icon_class": "fab fa-facebook"},
            {"name": "Twitter", "url": "https://twitter.com", "icon_class": "fab fa-twitter"},
            {"name": "Instagram", "url": "https://instagram.com", "icon_class": "fab fa-instagram"},
        ]

        about_page_content = f"""
        <section>
          <h2>Welcome to {site_title}</h2>
          <p>At {site_title}, we foster meaningful discussions and share knowledge that inspires innovation.</p>
          <h3>Our Mission</h3>
          <p>We aim to connect like-minded individuals through engaging content, deep conversations, and a collaborative environment.</p>
          <h3>Our Values</h3>
          <ul>
            <li><strong>Knowledge Sharing</strong> – We thrive on exchanging insights and learning.</li>
            <li><strong>Community-Driven</strong> – Your voice matters; together, we build a vibrant space.</li>
            <li><strong>Innovation &amp; Growth</strong> – Adapting and evolving with the latest trends and ideas.</li>
          </ul>
          <h3>Meet the Founder</h3>
          <p>{author} envisioned {site_title} as a space for creativity and intellectual exchange, ensuring a seamless blend of technology and dialogue.</p>
          <p>Want to join us? Stay connected and explore new possibilities!</p>
        </section>
        """

        if SiteConfig.objects.filter(active=True).exists():
            self.stdout.write(self.style.WARNING("An active SiteConfig already exists."))
            return

        # Create shared recommender settings
        recommender_settings = RecommenderSettings.objects.create(
            weight_user=0.2,
            weight_item=0.3,
            weight_content=0.5,
            cache_timeout=3600
        )

        theme = None
        theme_name = options.get("theme")

        if theme_name:
            try:
                theme = Theme.objects.get(name=theme_name)
                self.stdout.write(self.style.SUCCESS(f"Using theme: {theme.name}"))
            except Theme.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Theme '{theme_name}' not found — continuing without it."))

        # Create site config
        config = SiteConfig.objects.create(
            site_title=site_title,
            slug=slug,
            current_year=current_year,
            contact_email=contact_email,
            contact_phone=contact_phone,
            author=author,
            active=True,
            social_links=social_links,
            about_page_content=about_page_content,
            recommender_settings=recommender_settings,
            theme=theme
        )

        self.stdout.write(self.style.SUCCESS(f"SiteConfig for '{config.site_title}' created successfully."))

        default_tags = ["Technology", "Innovation", "Community", "AI", "Development"]
        for tag_name in default_tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                slug=slugify(tag_name),
                site=config
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created tag: {tag.name}"))
            else:
                self.stdout.write(f"Tag already exists: {tag.name}")
