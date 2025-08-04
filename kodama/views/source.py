from django.shortcuts import render, get_object_or_404
from kodama.models import Source
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from kodama.serializers import SourceSerializer
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse
from kodama.page import PageProcessor


def source_list(request, site):
    """View to display all Sources scoped to a site."""
    sources = Source.objects.all().order_by('title')
    context = {
        "page_title": "Sources",
        "sources": sources,
    }
    processor = PageProcessor(site)

    return render(
        request,
        "kodama/sources.html",
        processor.decorate(context, request)
    )

def source_detail(request, site, pk):
    """View to display a single Source scoped to a site."""
    source = get_object_or_404(Source, pk=pk)
    processor = PageProcessor(site)

    context = {
        "page_title": source.title,
        "source": SourceSerializer(source, context={'request': request}).data
    }

    return render(
        request,
        "kodama/source_detail.html",
        processor.decorate(context, request)
    )