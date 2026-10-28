from django.shortcuts import render
from django.views.generic import ListView
from .models import Course

class CourseListView(ListView):
    model = Course
    template_name = "courses/list_view.html"
    context_object_name = "courses"
    paginate_by = 1