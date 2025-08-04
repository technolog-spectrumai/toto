from celery import shared_task
import logging
from .recommend import RecommendationEngine
from .models import SiteConfig
from .audit import task_audit
from .models import TaskAudit

logger = logging.getLogger("django")


@shared_task(bind=True)
def update_recommendation_cache(arg):
    with task_audit(task_name="update_recommendation_cache-2") as audit:
        logger.info("Task started: rebuilding recommendation data")
        for site_config in SiteConfig.objects.filter(active=True):
            settings = site_config.recommender_settings
            if not settings:
                logger.warning(f"No recommender settings found for site '{site_config.slug}' — skipping.")
                continue
            recommender = RecommendationEngine.create(settings)
            recommender.build(site_config)
            logger.info(f"Updated recommendations for site: {site_config.slug}")
        logger.info("Task finished: rebuilding recommendation data")
        audit.result = "SUCCESS"
