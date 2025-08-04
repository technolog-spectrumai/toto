from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Tag
from django.core.cache import cache
from .models import SiteConfig
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.http import require_POST
import logging
from .serializers import (SiteConfigSerializer, CategorySerializer, TagSerializer)
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.urls import reverse


logger = logging.getLogger("django")


class PageProcessor:
    """Processes per-site data for views using serializers."""

    def __init__(self, site_slug):
        self.site_slug = site_slug
        self.site_config = self._load_site_config()

    def _load_site_config(self):
        site = get_object_or_404(SiteConfig, slug=self.site_slug, active=True)
        return SiteConfigSerializer(site).data

    def get_footer_data(self):
        prefix = "kodama"
        return {
            "contact_details": [
                {
                    "name": "Email",
                    "url": f"mailto:{self.site_config['contact_email']}",
                    "icon_class": "fas fa-envelope"
                },
                {
                    "name": "Phone",
                    "url": f"tel:{self.site_config['contact_phone']}",
                    "icon_class": "fas fa-phone"
                },
            ],
            "footer_links": [
                {"name": "Home", "url": f"/{prefix}/{self.site_slug}/"},
                {"name": "About Us", "url": f"/{prefix}/{self.site_slug}/about"},
                {"name": "Blog", "url": f"/{prefix}/{self.site_slug}/"},
                {"name": "Contact", "url": f"/{prefix}/{self.site_slug}/contact"},
            ],
            "social_links": self.site_config["social_links"],
        }

    def get_header_data(self, request):
        prefix = "kodama"
        categories = Category.objects.filter(site__slug=self.site_slug)
        serialized_categories = CategorySerializer(categories, many=True).data

        nav_links = [
            {"name": "Home", "url": f"/{prefix}/{self.site_slug}/", "icon": "fa fa-home"},
            {
                "name": "Categories",
                "dropdown": [
                    {
                        "name": cat['name'],
                        "url": f"/{prefix}/{self.site_slug}/category/{cat['slug']}",
                        "icon": "fa fa-folder"
                    } for cat in serialized_categories
                ],
                "icon": "fa fa-list"
            },
            {"name": "Sources", "url": f"/{prefix}/{self.site_slug}/sources/", "icon": "fa fa-book"},
        ]

        # Append auth links directly to nav_links
        if request.user.is_authenticated:
            nav_links.extend([
                {"name": "Logout", "url": reverse('kodama_logout', args=[self.site_slug]),
                 "icon": "fas fa-sign-out-alt"},
                {
                    "name": "Your Profile",
                    "url": reverse('profile_detail', args=[self.site_slug, request.user.username]),
                    "icon": "fas fa-user"
                }
            ])
        else:
            nav_links.append({
                "name": "Login",
                "url": reverse('kodama_login', args=[self.site_slug]),
                "icon": "fas fa-sign-in-alt"
            })

        return {
            "nav_links": nav_links,
            "user_logged_in": request.user.is_authenticated,
        }

    def decorate(self, data, request):
        categories = Category.objects.filter(site__slug=self.site_slug)
        tags = Tag.objects.filter(site__slug=self.site_slug)
        data.update({
            "categories": CategorySerializer(categories, many=True).data,
            "tags": TagSerializer(tags, many=True).data,
            "header": self.get_header_data(request),
            "footer": self.get_footer_data(),
            "site": self.site_config,
            "show_search": True,
            "theme": self.site_config["theme"]["theme"],
            "font": self.site_config["theme"]["font"]
        })
        return data

    def get_basic_data(self, request):
        return {
            "header": self.get_header_data(request),
            "footer": self.get_footer_data(),
            "site": self.site_config,
            "show_search": False,
            "theme": self.site_config["theme"]["theme"],
            "font": self.site_config["theme"]["font"]
        }



