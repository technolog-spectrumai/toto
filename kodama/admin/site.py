from django.contrib import admin
from django import forms
from django_tiptap.widgets import TipTapWidget
from kodama.models import  SiteConfig
from django.contrib import messages
from kodama.recommend import RecommendationEngine
import logging


logger = logging.getLogger("django")


class SiteConfigAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.enable_wysiwyg:
            self.fields['about_page_content'].widget = forms.Textarea(attrs={'rows': 10})
        else:
            self.fields['about_page_content'].widget = TipTapWidget()

    class Meta:
        model = SiteConfig
        fields = '__all__'


@admin.action(description="Rebuild recommendation scores")
def rebuild_recommendations(modeladmin, request, queryset):
    for site_config in queryset.filter(active=True):
        try:
            settings = site_config.recommender_settings
            if not settings:
                logger.warning(f"No recommender settings found for site '{site_config.slug}' — skipping.")
            else:
                recommender = RecommendationEngine.create(settings)
                recommender.build(site_config)
        except Exception as e:
            messages.warning(request, f"Failed to rebuild for {site_config}: {e}")
    messages.success(request, f"Rebuilt recommendations")



@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    form = SiteConfigAdminForm

    list_display = (
        'site_title', 'slug', 'current_year',
        'contact_email', 'contact_phone',
        'author', 'active', 'measure_read_time',
        'theme'
    )
    list_filter = ('active', 'measure_read_time')
    search_fields = ('site_title', 'author', 'contact_email', 'slug', 'theme__name')
    ordering = ('-current_year',)
    prepopulated_fields = {'slug': ('site_title',)}
    actions = [rebuild_recommendations]

    fieldsets = (
        (None, {
            "fields": (
                'site_title', 'slug', 'current_year',
                'contact_email', 'contact_phone', 'author', 'active',
                'theme'  # 👉 edit theme inline
            )
        }),
        ("WYSIWYG & Content", {
            "classes": ("collapse",),
            "fields": ('enable_wysiwyg', 'about_page_content')
        }),
        ("Settings", {
            "classes": ("collapse",),
            "fields": (
                'num_latest', 'num_recommendations',
                'cache_lifetime', 'measure_read_time',
                'recommender_settings'
            )
        }),
        ("Social & Branding", {
            "classes": ("collapse",),
            "fields": ('social_links',)
        }),
    )
