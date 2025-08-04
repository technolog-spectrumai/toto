from django.urls import path
from . import views

urlpatterns = [
    # Site-specific (scoped under site slug)
    path('<slug:site>/', views.latest_articles, name='site_home'),
    path('<slug:site>/articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('<slug:site>/articles/<slug:slug>/feedback/', views.article_feedback, name='article_feedback'),
    path('<slug:site>/contact/', views.contact_view, name='contact'),
    path('<slug:site>/about/', views.about_view, name='about'),
    path('<slug:site>/category/<slug:slug>/', views.category_view, name='articles_by_category'),
    path('<slug:site>/tag/<slug:slug>/', views.tag_view, name='articles_by_tag'),
    path('<slug:site>/latest/', views.latest_articles, name='latest_articles'),
    path('<slug:site>/search/', views.search_articles, name='article_search'),

    path('<slug:site>/src/<int:pk>/', views.source_detail, name='source_detail'),
    path('<slug:site>/sources/', views.source_list, name='source_list'),

    path('<slug:site>/author/<str:username>/', views.author_profile, name='author_profile'),
    path("<slug:site>/profile/<str:username>/", views.profile_detail, name="profile_detail"),

    path("<slug:site>/logout/", views.logout_view, name="kodama_logout"),
    path("<slug:site>/login/", views.login_view, name="kodama_login"),
    path('<slug:site>/goodbye/', views.goodbye_view, name="goodbye"),

    # Catch-all 404 for unmatched routes
    path('<slug:site>/<path:unmatched>/', views.custom_404_view, name="custom_404"),
    path('<path:unmatched>/',
         lambda request, unmatched: views.custom_404_view(request, site="Unknown", unmatched=unmatched)),
]
