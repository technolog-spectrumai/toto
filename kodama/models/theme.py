from django.db import models
from django_jsonform.models.fields import JSONField

_SCHEMA = {
    "type": "array",
    "title": "Tailwind Structural Tokens",
    "items": {
        "type": "object",
        "properties": {
            "element": {
                "type": "string",
                "enum": [
                    "body", "header", "footer", "navbar_wrapper", "navbar_title", "nav_link",
                    "nav_dropdown", "toggle_button", "mobile_nav_panel", "latest_intro",
                    "login_box", "profile_wrapper", "profile_field_label", "profile_field_value",
                    "profile_divider", "profile_footer", "search_intro_text", "search_empty_text",
                    "tag_title", "tag_intro", "tag_empty_text", "source_card",
                    "source_detail_box", "source_divider", "source_field_label",
                    "source_field_value", "source_back_button", "footer_link", "section_title",
                    "footer_notice", "search_field", "search_submit", "login_title",
                    "login_input", "login_button", "login_link", "draft_badge", "meta_text",
                    "image_border", "image_caption", "author_link", "edit_button",
                    "category_badge", "abstract_box", "content_box", "tag_link", "home_link",
                    "like_button", "like_count_text", "dislike_button", "dislike_count_text",
                    "section_divider", "category_link", "source_link",
                    "add_source_button", "source_footer_border", "source_divider", "email_link", "company_card",
                    "profile_back_button", "library_link", "section_body"
                ]
            },
            "mode": {
                "type": "string",
                "enum": ["light", "dark"]
            },
            "class": {
                "type": "string",
                "title": "Tailwind Classes",
                "description": "Full Tailwind class list for this element in this mode"
            }
        },
        "required": ["element", "mode", "class"]
    }
}


class Font(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        help_text="Display name of the font (e.g. 'Playfair Display')"
    )
    cdn_link = models.URLField(
        help_text="CDN or stylesheet URL for importing the font (e.g. Google Fonts)"
    )

    def __str__(self):
        return self.name


class Theme(models.Model):

    SCHEMA = _SCHEMA
    name = models.CharField(
        max_length=64,
        unique=True,
        help_text="Name of the theme"
    )

    theme = JSONField(
        schema=_SCHEMA,
        default=[],
        help_text="Tailwind classes for page-level layout elements"
    )
    font = models.ForeignKey(
        Font,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="themes",
        help_text="Font applied to this theme"
    )

    def __str__(self):
        return self.name
