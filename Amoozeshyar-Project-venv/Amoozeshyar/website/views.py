from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.
def MainView(request):
    return render(request, "main.html")

def StudentFormView(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            new_student = form.save(commit=False)
            set_entrance_year(student, new_student)
            set_last_year(student, new_student)
            set_student_number(student, new_student)

            new_user = User.objects.create_user(
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                username=new_student.student_number,
                password=str(new_student.date_of_birth)[:4]
            )

            new_student.user = new_user
            new_student.save()

            return render(request, "main.html", {"message":"ثبت نام موفقیت آمیز بود"})
    else:
        form = StudentForm()

    return render(request, "register_student.html", {"form":form})


def ProfessorFormView(request):
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES)
        if form.is_valid():
            new_professor = form.save(commit=False)

            set_created(professor, new_professor)
            set_professor_code(professor, new_professor)


            new_user = User.objects.create_user(
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                username = new_professor.professor_code,
                password=str(form.cleaned_data["date_of_birth"])[:4]
            )


            new_professor.user = new_user
            new_professor.save()
            new_professor.universities.set(form.cleaned_data["universities"])
            
            return render(request, "main.html", {"message":"ثبت نام موفقیت آمیز بود"})
    else:
        form = ProfessorForm()

    return render(request, "register_professor.html", {"form":form})