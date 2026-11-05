from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "community/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "community/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("community:detail", kwargs={"pk": self.object.pk})

    class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
        def test_func(self):
         return self.get_object().author_id == self.request.user.pk


class PostUpdateView(OwnerRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "community/post_form.html"

    def get_success_url(self):
        return reverse("community:detail", kwargs={"pk": self.object.pk})


class PostDeleteView(OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = "community/post_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("community:feed")