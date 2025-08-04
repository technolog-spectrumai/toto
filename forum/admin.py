from django.contrib import admin
from .models import Topic, Post

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Shows title and creation date
    search_fields = ('title',)  # Enables searching by title
    ordering = ('-created_at',)  # Sorts by newest first


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'parent', 'author', 'content_preview', 'depth', 'created_at')  # Added depth field
    search_fields = ('content', 'author__username')  # Search by content & author
    list_filter = ('created_at', 'author', 'topic', 'depth')  # Allow filtering by depth
    ordering = ('-created_at',)  # Sorts by most recent first
    list_editable = ('parent',)  # Allows quick assignment of parent post
    list_display_links = ('topic',)  # Topic is clickable for navigation
    readonly_fields = ('depth',)  # Prevent manual editing of depth

    def get_queryset(self, request):
        """Optimize queries for better performance."""
        return super().get_queryset(request).select_related('parent', 'author', 'topic')

    @admin.display(description="Content Preview")
    def content_preview(self, obj):
        """Display a short preview of post content in admin."""
        return obj.content[:50] + "..." if obj.content else "No content"
