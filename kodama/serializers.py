from rest_framework import serializers
from .models import SiteConfig, Category, Tag, Article, AuthorProfile, Source, ArticleImage, Theme, Section
from django.utils import formats
from django.utils.html import strip_tags


class ThemeSerializer(serializers.ModelSerializer):
    font = serializers.CharField(source='font.name', read_only=True)

    class Meta:
        model = Theme
        fields = ["id", "name", "theme", "font"]


class SiteConfigSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)
    class Meta:
        model = SiteConfig
        fields = [
            'id', 'slug', 'site_title', 'current_year',
            'contact_email', 'contact_phone', 'author',
            'about_page_content', 'social_links', 'measure_read_time', "theme"
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class AuthorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = AuthorProfile
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'bio', 'profile_picture', 'date_joined'
        ]

    def get_date_joined(self, obj):
        return formats.date_format(obj.date_joined, format='DATE_FORMAT', use_l10n=True)


class SourceSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    publication_date = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            'title', 'creator', 'publication_date',
            'type', 'url', 'pk'
        ]

    def get_publication_date(self, obj):
        return formats.date_format(obj.publication_date, format='DATE_FORMAT', use_l10n=True)


class ArticleImageSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    class Meta:
        model = ArticleImage
        fields = ['title', 'slug', 'file', 'source']


class SectionSerializer(serializers.ModelSerializer):
    image = ArticleImageSerializer(read_only=True)

    class Meta:
        model = Section
        fields = [
            'order',
            'title',
            'content',
            'image'
        ]


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = AuthorProfileSerializer(read_only=True)
    image = ArticleImageSerializer(read_only=True)
    word_count = serializers.ReadOnlyField()
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'title',
            'author',
            'slug',
            'created_at',
            'abstract',
            'tags',
            'word_count',
            'is_draft',
            'image',
            'sections'
        ]


class ContactSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = ['site_title', 'contact_email', 'contact_phone']







