from .site import (
    custom_404_view,
    login_view,
    goodbye_view,
    logout_view,
    contact_view,
    about_view,
)

from .article import (
    latest_articles,
    article_detail,
    article_feedback,
    category_view,
    tag_view,
    search_articles
)

from .profile import (
    profile_detail,
    author_profile,
)

from .source import (
    source_list,
    source_detail
)


__all__ = [
    # Site views
    "custom_404_view",
    "login_view",
    "goodbye_view",
    "logout_view",
    "contact_view",
    "about_view",

    # Article views
    "latest_articles",
    "article_detail",
    "article_feedback",
    "category_view",
    "tag_view",
    "search_articles",

    # Author views
    "profile_detail",
    "author_profile",

    # source views
    "source_list",
    "source_detail"
]
