from django.urls import path

from .views import FeedView, PostCreateView, PostDeleteView, PostUpdateView, post_detail, mark_solution


app_name = "community"

urlpatterns = [
    path("", FeedView.as_view(), name="feed"),
    path("publicar/", PostCreateView.as_view(), name="create"),
    path("publicacao/<int:pk>/", post_detail, name="detail"),
    path("publicacao/<int:pk>/editar/", PostUpdateView.as_view(), name="edit"),
    path("publicacao/<int:pk>/excluir/", PostDeleteView.as_view(), name="delete"),
    path("resposta/<int:answer_id>/solucao/", mark_solution, name="mark_solution"),
]