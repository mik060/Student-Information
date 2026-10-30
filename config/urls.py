from django.contrib import admin
from django.urls import path
from students import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:student_id>/delete/", views.delete_student, name="delete_student"),
]
