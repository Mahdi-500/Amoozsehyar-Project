from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
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

            messages.success(request, "ثبت نام موفقیت آمیز بود")
            return redirect('website:main') 

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
            
            messages.success(request, "ثبت نام موفقیت آمیز بود")
            return redirect('website:main')
    else:
        form = ProfessorForm()

    return render(request, "register_professor.html", {"form":form})


def LessonFormView(request):
    if request.method == "POST":
        form = LessonForm(request.POST)

        if form.is_valid():
            new_lesson = form.save(commit=False)
            set_lesson_code(lesson, new_lesson)

            new_lesson.save()
            new_lesson.pishniaz.set(form.cleaned_data["pishniaz"])
            new_lesson.hamniaz.set(form.cleaned_data["hamniaz"])

            messages.success(request, "ثبت درس موفقیت آمیز بود")
            return redirect('website:main')
        
    else:
        form = LessonForm()
    
    return render(request, "register_professor.html", {'form':form})



def LessonClassFromView(request):
    if request.method == "POST":
        form = LessonClassFrom(request.POST)
        #flag = False

        if form.is_valid():

            day = form.cleaned_data["lesson_day"]
            time = form.cleaned_data["lesson_time"]
            class_number = form.cleaned_data["class_number"]
            semester = form.cleaned_data["semester"]

            # ? checking class overlap
            classes = lesson_class.objects.all().filter(semester=semester,
                                                        lesson_day=day,
                                                        lesson_time=time,
                                                        class_number=class_number,
                                                        )
            if classes:
                form = LessonClassFrom(request.POST)
                messages.error(request, f"زمان و روز برگزاری این کلاس با  {classes[0]}  تداخل دارد")
                return render(request, "add_lesson_class.html", {'form':form})
        
            # ? alternative way for checking class overlap
            #classes = lesson_class.objects.all()
            # for i in classes:
            #     if i.semester == semester:
            #         if i.lesson_day == day:
            #             if i.lesson_time == time:
            #                 if i.class_number == class_number:
            #                     flag = True
            
            # if not flag:
            #     form.save()
            #     messages.success(request, "کلاس با موفقیت ایجاد شد")
            #     return redirect("website:main")
            # else:
            #     form = LessonClassFrom(request.POST)
            #     messages.error(request, "زمان و روز برگزاری این کلاس با یک کلاس دیگر تداخل دارد")
            #     messages.info(request, i)
            #     return render(request, "add_lesson_class.html", {'form':form})
            
    else:
        form = LessonClassFrom()
    return render(request, "add_lesson_class.html", {'form':form})
