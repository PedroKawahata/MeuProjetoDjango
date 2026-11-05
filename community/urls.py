from django.urls import path

from .views import FeedView, PostCreateView, PostDetailView


app_name = "community"

urlpatterns = [
    path("", FeedView.as_view(), name="feed"),
    path("publicar/", PostCreateView.as_view(), name="create"),
    path("publicacao/<int:pk>/", PostDetailView.as_view(), name="detail"),
]