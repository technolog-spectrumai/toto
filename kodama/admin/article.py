from django.contrib import admin
from django import forms
from django_tiptap.widgets import TipTapWidget
from kodama.models import Article, AuthorProfile, Category, SiteConfig, Tag, Section
from django.utils.html import format_html
from .section import SectionAdminForm


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'site')
    list_filter = ('site',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class SectionInline(admin.StackedInline):
    form = SectionAdminForm
    model = Section
    extra = 1
    fields = ('order', 'title', 'content', 'image')
    ordering = ('order',)
    show_change_link = True


class ArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can base this on a model field, a global setting, or site config
        config = SiteConfig.objects.first()
        use_wysiwyg = getattr(config, "enable_wysiwyg", True)

        if not use_wysiwyg:
            self.fields['abstract'].widget = forms.Textarea(attrs={'rows': 15})
        else:
            self.fields['abstract'].widget = TipTapWidget()

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    inlines = [SectionInline]

    list_display = (
        'title',
        'version',
        'is_draft',
        'author',
        'site',
        'created_at',
        'display_image',
        'word_count_display',
        'section_count',
    )
    list_filter = (
        'site',
        'created_at',
        'categories',
        'tags',
        'is_draft',
    )
    search_fields = (
        'title',
        'slug',
        'abstract',
        'author__user__username',
        'version',
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    filter_horizontal = (
        'categories',
        'tags',
        'sources',
    )

    readonly_fields = ('word_count_display',)

    def word_count_display(self, obj):
        return f"{obj.word_count:,} words"
    word_count_display.short_description = "Word Count"

    def display_image(self, obj):
        if obj.image and obj.image.file:
            return format_html('<img src="{}" width="100" height="auto"/>', obj.image.file.url)
        return "-"
    display_image.short_description = "Thumbnail"

    def section_count(self, obj):
        return obj.sections.count()
    section_count.short_description = "Sections"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'site')
    list_filter = ('site',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_joined')
