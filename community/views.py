from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Post


class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "community/feed.html"
    context_object_name = "posts"
    paginate_by = 10