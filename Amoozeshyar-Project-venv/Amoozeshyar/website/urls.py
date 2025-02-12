from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("", views.MainView, name="main"),
    path("register-student", views.StudentFormView, name="register_student"),
    path("register-professor", views.ProfessorFormView, name="register_professor"),
]
