from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from courses.forms import CourseForm
from courses.models import Course


class CourseListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = Course
    context_object_name = "courses"
    paginate_by = 10
    permission_required = "courses.view_course"


class CourseDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"
    permission_required = "courses.view_course"


class CourseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form_create.html"
    success_url = reverse_lazy("courses:course_list")
    permission_required = "courses.add_course"


class CourseUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form_update.html"
    context_object_name = "course"
    success_url = reverse_lazy("courses:course_list")
    permission_required = "courses.change_course"


class CourseDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    context_object_name = "course"
    success_url = reverse_lazy("courses:course_list")
    permission_required = "courses.delete_course"