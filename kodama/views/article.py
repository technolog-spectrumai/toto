from django.shortcuts import render, get_object_or_404
from kodama.models import Article, Category, Tag, Hit
from django.core.cache import cache
from kodama.models import SiteConfig, ArticleFeedback
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.db.models import Q
import re
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from kodama.recommend import RecommendationEngine
import logging
from kodama.serializers import ArticleSerializer
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse
from kodama.page import PageProcessor


logger = logging.getLogger("django")


def _get_visible_articles(user=None):
    if user and user.is_authenticated:
        return Article.objects.filter(
            Q(is_draft=False) | Q(author__user=user)
        )
    return Article.objects.filter(is_draft=False)


def latest_articles(request, site):
    processor = PageProcessor(site)
    site_config = get_object_or_404(SiteConfig, slug=site)
    latest_qs = _get_visible_articles(request.user).order_by("-created_at")[:site_config.num_latest]
    latest_serialized = ArticleSerializer(latest_qs, many=True).data
    recommended = []
    settings = site_config.recommender_settings
    if settings and request.user.is_authenticated:
        recommender = RecommendationEngine.create(settings)
        recommended = recommender.predict(user=request.user, site=site_config)

    context = {
        "page_title": "Latest Articles",
        "articles": latest_serialized,
        "recommended": ArticleSerializer(recommended, many=True).data
    }
    return render(request, "kodama/latest.html", processor.decorate(context, request))


def article_detail(request, site, slug):
    """View to display a single article scoped to a site, with ordered sections and feedback."""

    article = get_object_or_404(Article, slug=slug)

    # Feedback counts
    like_count = ArticleFeedback.objects.filter(article=article, liked=True).count()
    dislike_count = ArticleFeedback.objects.filter(article=article, liked=False).count()

    # Reading time estimates
    speed = 250  # Words per minute
    word_count = article.word_count
    minutes = word_count // speed
    seconds = int((word_count / speed - minutes) * 60)

    context = {
        "page_title": article.title,
        "article": ArticleSerializer(article).data,
        "reader": {
            "speed": speed,
            "word_count": word_count,
            "minutes": minutes,
            "seconds": seconds
        },
        "feedback": {
            "like_count": like_count,
            "dislike_count": dislike_count
        }
    }

    # View tracking if enabled
    processor = PageProcessor(site)
    if processor.site_config.get("measure_read_time"):
        Hit.log_if_allowed(request, article)

    return render(request, "kodama/article_detail.html", processor.decorate(context, request))


@require_POST
@login_required
def article_feedback(request, site, slug):
    """Handle feedback on an article, scoped to a specific site."""
    article = get_object_or_404(Article, slug=slug, site__slug=site)

    liked = request.POST.get("liked") == "true"

    ArticleFeedback.objects.update_or_create(
        user=request.user,
        article=article,
        defaults={"liked": liked}
    )

    return redirect("article_detail", site=site, slug=article.slug)


def category_view(request, site, slug):
    """View to display articles by category, scoped to a specific site."""
    processor = PageProcessor(site)

    category = get_object_or_404(Category, slug=slug, site__slug=site)
    articles = _get_visible_articles(request.user).filter(categories=category)
    recommended = []
    site_config = get_object_or_404(SiteConfig, slug=site)
    include_list = [article.id for article in articles]
    settings = site_config.recommender_settings
    if settings and request.user.is_authenticated:
        recommender = RecommendationEngine.create(settings)
        recommended = recommender.predict(user=request.user, site=site_config, include_list=include_list)

    context = {
        "page_title": f"Category: {category.name}",
        "articles": articles,
        "category": category,
        "recommended": ArticleSerializer(recommended, many=True).data
    }

    return render(request, "kodama/category.html", processor.decorate(context, request))


def tag_view(request, site, slug):
    """View to display articles by tag, scoped to a specific site."""
    processor = PageProcessor(site)

    tag = get_object_or_404(Tag, slug=slug, site__slug=site)
    articles = _get_visible_articles(request.user).filter(tags=tag)
    context = {
        "page_title": f"Tag: {tag.name}",
        "articles": articles,
        "tag": tag,
    }

    return render(request, "kodama/tag.html", processor.decorate(context, request))


def search_articles(request, site):
    """Search across articles for a given site based on user query."""
    query = request.GET.get("q", "").strip()
    keywords = re.findall(r'\w+', query.lower())

    search_filter = Q()
    for word in keywords:
        search_filter |= Q(title__icontains=word)
        search_filter |= Q(abstract__icontains=word)
        search_filter |= Q(tags__name__icontains=word)
        search_filter |= Q(categories__name__icontains=word)
        search_filter |= Q(author__user__username__icontains=word)

    results = _get_visible_articles(request.user).filter(search_filter).distinct()

    context = {
        "query": query,
        "articles": results,
        "page_title": f"Search: {query}",
    }

    processor = PageProcessor(site)
    return render(request, "kodama/query.html", processor.decorate(context, request))




