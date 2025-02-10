from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.
def MainView(request):
    temp = student.objects.all()
    year = str(temp[0].entrance_year)[1:4]
    return render(request, "main.html", {"info":year})

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

            raise NameError
    else:
        form = StudentForm()

    return render(request, "main.html", {"form":form})