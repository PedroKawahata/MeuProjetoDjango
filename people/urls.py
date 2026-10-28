from django.urls import path
from .views import PersonListView  # Importa a view da PRÓPRIA pasta people

app_name = "people"  # Nome correto do app

urlpatterns = [
    path("people/", PersonListView.as_view(), name="person-list"),
    path("pessoas/", PersonListView.as_view(), name="person-list-pt"),
]