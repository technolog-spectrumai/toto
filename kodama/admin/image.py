from django.contrib import admin
from kodama.models import (ArticleImage)



@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'source')
    list_filter = ('source',)
    search_fields = ('title', 'slug', 'source__title')
    prepopulated_fields = {'slug': ('title',)}
