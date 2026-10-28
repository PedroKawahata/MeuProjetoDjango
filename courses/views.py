from django.shortcuts import render
from django.views.generic import ListView
from courses.models import Course, Person
# Create your views here.
class CourseListView(ListView):
    model = Course
    template_name = "courses/list_view.html"
    context_object_name = "courses"
    paginate_by = 1

class PersonListView(ListView):
    model = Person
    template_name = "courses/list_view.html"
    context_object_name = "people"
    paginate_by = 1