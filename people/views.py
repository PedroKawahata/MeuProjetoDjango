from django.shortcuts import render
from django.views.generic import ListView
from courses.models import Course, Person  # Certifique-se de que o modelo Person realmente vive em courses.models

class PersonListView(ListView):
    model = Person
    template_name = "person/list_view.html"
    context_object_name = "people"
    paginate_by = 1