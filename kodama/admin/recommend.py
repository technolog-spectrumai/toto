from django.contrib import admin
from kodama.models import RecommendationScores, RecommenderSettings


@admin.register(RecommendationScores)
class RecommendationScoresAdmin(admin.ModelAdmin):
    list_display = ('site', 'created_at', 'active')
    list_filter = ('site',)
    readonly_fields = ('created_at', )

@admin.register(RecommenderSettings)
class RecommenderSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'weight_user', 'weight_item', 'weight_content', 'cooldown_minutes')
    list_filter = ('cooldown_minutes', )
    search_fields = ('id',)