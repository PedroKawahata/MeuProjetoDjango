from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.views.decorators.http import require_POST

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