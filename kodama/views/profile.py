from django.shortcuts import render, get_object_or_404
from kodama.models import Article, AuthorProfile
from django.core.cache import cache
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
from kodama.serializers import AuthorProfileSerializer
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.urls import reverse
from kodama.page import PageProcessor


def profile_detail(request, site, username):
    user = get_object_or_404(User, username=username)

    profile = AuthorProfile.objects.filter(user=user).first()

    if not profile:
        profile = AuthorProfile(
            user=user,
            bio="",
            profile_picture=None,
            date_joined=user.date_joined if hasattr(user, "date_joined") else None
        )

    serializer = AuthorProfileSerializer(profile, context={'request': request})

    processor = PageProcessor(site)
    context = {
        "profile": serializer.data,
        "profile_obj": profile,
        "page_title": f"Profile: {user.get_full_name() or user.username}",
    }

    return render(request, "kodama/profile_detail.html", processor.decorate(context, request))


def author_profile(request, site, username):
    """View to display a single author's profile scoped to a specific site."""
    processor = PageProcessor(site)

    author_profile = get_object_or_404(AuthorProfile, user__username=username)
    authored_articles = Article.objects.filter(author=author_profile).order_by('-created_at')

    context = {
        "page_title": f"Profile of {author_profile.user.username}",
        "author": author_profile,
        "articles": authored_articles,
    }

    return render(request, "kodama/author.html", processor.decorate(context, request))