from django.urls import path
from courses.views import CourseListView, PersonListView

app_name = "courses"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("cursos/", CourseListView.as_view(), name="course-list-pt"),
]
   