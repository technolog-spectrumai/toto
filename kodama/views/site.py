from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from kodama.models import SiteConfig
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
import re
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from kodama.serializers import ContactSiteSerializer
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse
from kodama.page import PageProcessor


def custom_404_view(request, site=None, unmatched=None):
    """Multitenant-aware 404 error page."""
    processor = PageProcessor(site) if site else None

    context = {
        "page_title": "Page Not Found",
        "error_message": f"The page '{unmatched}' could not be found." if unmatched else "This page does not exist.",
    }

    if processor:
        context = processor.decorate(context, request)

    return render(request, "kodama/404.html", context, status=404)


def login_view(request, site):
    processor = PageProcessor(site)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("site_home", site=site)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "kodama/login.html", processor.get_basic_data(request))


def goodbye_view(request, site):
    processor = PageProcessor(site)
    return render(request, "kodama/goodbye.html", processor.get_basic_data(request))


def logout_view(request, site):
    logout(request)
    return redirect("goodbye", site=site)

def _send_contact_email(sender_name, sender_email, message, recipient_email):
    subject = f"New Contact Form Submission from {sender_name}"
    body = f"Message from {sender_name} ({sender_email}):\n\n{message}"

    send_mail(
        subject=subject,
        message=body,
        from_email=sender_email,
        recipient_list=[recipient_email],
        fail_silently=False
    )

def contact_view(request, site):
    processor = PageProcessor(site)
    site_obj = get_object_or_404(SiteConfig, slug=processor.site_slug, active=True)
    site_data = ContactSiteSerializer(site_obj).data

    if request.method == "POST":
        return redirect("contact", site=site)

    context = {
        "page_title": "Contact Us",
        **site_data,
    }

    return render(request, "kodama/contact.html", processor.decorate(context, request))


def about_view(request, site):
    """View to display the About Us page for a specific site."""
    processor = PageProcessor(site)

    context = {
        "page_title": "About Us",
        "about_html": processor.site_config["about_page_content"],
    }

    # Optional: clear site-specific cache if needed
    cache_key = f"site_config__{site}"
    cache.delete(cache_key)

    return render(request, "kodama/about.html", processor.decorate(context, request))