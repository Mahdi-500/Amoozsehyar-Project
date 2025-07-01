from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("", views.LoginFromView, name="login"),
    path("main/", views.MainView, name="main"),
    path("register-student", views.StudentFormView, name="register_student"),
    path("register-professor", views.ProfessorFormView, name="register_professor"),
    path("create_lesson", views.LessonFormView, name="create_lesson"),
    path("create_class", views.LessonClassFromView, name="lesson_class"),
    path("professor/profile", views.ProfessorProfile, name="professor_profile"),
    path("professor/classes/<str:p_code>/<str:u_code>", views.ProfessorLessonList, name="professor_lessons"),
    path('professor/lesson/details/<str:l_code>', views.LessonDetails, name="lesson_detail"),
    path("search", views.LessonSearchView, name="lesson_search"),
    path("choosing_lesson", views.ChoosingLessonFormView, name="choosing_lesson"),
    path("saving", views.SavingTheChosenLessonView, name="save"),
    path("professor/lesson/details/<str:l_code>/<int:class_code>/submitting_grade", views.GradeFormView, name="grade")
]
