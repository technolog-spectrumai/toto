from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import SiteConfig
from .recommender import Recommender
import logging

logger = logging.getLogger("django")

@receiver(post_migrate)
def populate_recommender_cache(sender, **kwargs):
    try:
        for site_config in SiteConfig.objects.filter(active=True):
            Recommender(site_config).populate_cache_from_db()
        logger.info("Recommender cache populated after migration.")
    except Exception as e:
        logger.warning(f"Error populating recommendation cache: {e}")
