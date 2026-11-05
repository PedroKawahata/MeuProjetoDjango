from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.views.decorators.http import require_POST
from django.db.models import Q

from .forms import AnswerForm, PostForm
from .models import Post,  Answer

@login_required
@require_POST
@transaction.atomic
def mark_solution(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    post = get_object_or_404(Post.objects.select_for_update(), pk=answer.post_id)

    if post.author_id != request.user.pk:
        raise PermissionDenied

    post.answers.filter(is_solution=True).update(is_solution=False)
    post.answers.filter(pk=answer.pk).update(is_solution=True)

    post.is_resolved = True
    post.save(update_fields=["is_resolved", "updated_at"])

    return redirect("community:detail", pk=post.pk)


class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "community/feed.html"
    context_object_name = "posts"
    paginate_by = 10
    def get_queryset(self):
        posts = Post.objects.select_related("author").order_by("-created_at", "-pk")
        search_term = self.request.GET.get("q", "").strip()
        selected_category = self.request.GET.get("category", "")

        if search_term:
            posts = posts.filter(
                Q(title__icontains=search_term)
                | Q(content__icontains=search_term)
                | Q(author__username__icontains=search_term)
            )

        if selected_category in dict(Post.CATEGORY_CHOICES):
            posts = posts.filter(category=selected_category)

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Post.CATEGORY_CHOICES
        context["search_term"] = self.request.GET.get("q", "").strip()
        context["selected_category"] = self.request.GET.get("category", "")
        return context


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.post = post
            answer.author = request.user
            answer.save()
            return redirect("community:detail", pk=post.pk)
    else:
        form = AnswerForm()

    return render(
        request,
        "community/post_detail.html",
        {
            "post": post,
            "answers": post.answers.select_related("author"),
            "answer_form": form,
        },
    )


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