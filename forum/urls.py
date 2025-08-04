from django.urls import path
from .views import thread_view, thread_list_view

urlpatterns = [
    path('thread/<int:thread_id>/', thread_view, name='thread_view'),
    path("threads/", thread_list_view, name="thread_list"),
]
