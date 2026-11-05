from django.urls import path
from courses.views import CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("<int:pk>/ver/", CourseDetailView.as_view(), name="course_detail"),
    path("criar/", CourseCreateView.as_view(), name="course_create"),
    path("<int:pk>/editar/", CourseUpdateView.as_view(), name="course_update"),
     path("<int:pk>/deletar/", CourseDeleteView.as_view(), name="course_delete"),
]
   