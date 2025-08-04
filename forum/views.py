from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Post


def thread_view(request, thread_id):
    thread = get_object_or_404(Topic, id=thread_id)
    posts = Post.objects.filter(topic=thread, parent=None).order_by("created_at")  # Show only root posts
    threads = Topic.objects.all().order_by("-created_at")

    if request.method == "POST":
        post_id = request.POST.get("post_id")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        parent_post = Post.objects.filter(id=post_id).first()

        if parent_post and parent_post.depth >= 3:
            return redirect(request.path)  # Prevent replies if depth limit is reached

        Post.objects.create(topic=thread, author=request.user, content=content, image=image, parent=parent_post)
        return redirect(request.path)

    return render(request, "forum/thread.html", {"thread": thread, "posts": posts, "threads": threads, "app_name": "forum"})


def thread_list_view(request):
    """Display a list of all threads."""
    threads = Topic.objects.all().order_by("-created_at")
    return render(request, "forum/thread_list.html", {"threads": threads, "app_name": "forum"})
