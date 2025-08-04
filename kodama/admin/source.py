from django.contrib import admin
from kodama.models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creator', 'publication_date')
    list_filter = ('type', 'publication_date')
    search_fields = ('title', 'creator')
    ordering = ('-publication_date',)