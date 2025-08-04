from django.contrib import admin
from kodama.models import SiteConfig, Hit, ArticleFeedback
from django.contrib import messages
from kodama.recommend import RecommendationEngine


@admin.register(Hit)
class HitAdmin(admin.ModelAdmin):
    list_display = (
        'article', 'user', 'ip_address', 'timestamp',
    )
    list_filter = (
        'timestamp', 'article',
    )
    search_fields = (
        'user__username', 'ip_address', 'user_agent', 'article__title',
    )
    readonly_fields = (
        'article', 'user', 'ip_address', 'user_agent', 'timestamp',
    )
    ordering = ('-timestamp',)


@admin.register(ArticleFeedback)
class ArticleFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'liked', 'timestamp')
    list_filter = ('liked', 'timestamp', 'user')
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('timestamp',)
    actions = ['rebuild_recommendations_for_selected']

    def rebuild_recommendations_for_selected(self, request, queryset):
        site_ids = set(queryset.values_list('article__site_id', flat=True).distinct())
        updated = 0
        self.message_user(request, f"site_ids {site_ids}", level=messages.WARNING)
        for site_id in site_ids:
            try:
                site_config = SiteConfig.objects.get(id=site_id)
                settings = getattr(site_config, 'recommender_settings', None)
                if settings:
                    recommender = RecommendationEngine.create(settings)
                    recommender.build(site_config)
                    updated += 1
                else:
                    self.message_user(request, f"No recommender settings for site ID {site_id}", level=messages.WARNING)
            except SiteConfig.DoesNotExist:
                self.message_user(request, f"SiteConfig not found for site ID {site_id}", level=messages.ERROR)

        self.message_user(request, f"Updated recommendations for {updated} site(s).", level=messages.SUCCESS)

    rebuild_recommendations_for_selected.short_description = "Build recommendations for selected feedback"