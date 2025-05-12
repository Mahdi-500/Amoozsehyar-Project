from django.db.models import Q
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import *
from .forms import *

# Create your views here.
def MainView(request):
    user = User.objects.get(username=request.user.username)
    user_group = user.groups.get()
    return render(request, "main.html", {"group":user_group, "user":user})



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
            
            # ? adding a group
            if not Group.objects.filter(name='student').exists():
                Group.objects.create(name='student')

            student_group = Group.objects.get(name='student')
            new_student.user.groups.add(student_group)

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
                username = new_professor.code,
                password=str(form.cleaned_data["date_of_birth"])[:4]
            )


            new_professor.user = new_user
            new_professor.save()
            new_professor.universities.set(form.cleaned_data["universities"])

            # ? adding a group
            if not Group.objects.filter(name='professor').exists():
                Group.objects.create(name='professor')

            professor_group = Group.objects.get(name='professor')
            new_professor.user.groups.add(professor_group)
            
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
            
            new_lesson_class = form.save(commit=False)
            day = form.cleaned_data["lesson_day"]
            time = form.cleaned_data["lesson_time"]
            class_number = form.cleaned_data["class_number"]
            semester = form.cleaned_data["semester"]
            class_location = form.cleaned_data["university_location"]

            if semester == None:
                set_semester(lesson_class, new_lesson_class)
                semester = new_lesson_class.semester


            # ? checking class overlap
            classes = lesson_class.objects.filter(semester=semester,
                                                        lesson_day=day,
                                                        lesson_time=time,
                                                        class_number=class_number,
                                                        university_location=class_location
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
            
            try:
                form.save()
            except IntegrityError:
                messages.error(request, "این کد ارائه در این نیمسال وجود دارد")
                form = LessonClassFrom(request.POST)
                return render(request, "add_lesson_class.html", {'form':form})
            
            messages.success(request, "کلاس با موفقیت ایجاد شد")
            return redirect("website:main")
        
    else:
        form = LessonClassFrom()
        return render(request, "add_lesson_class.html", {'form':form})
    
    return render(request, "add_lesson_class.html", {'form':form})




def LoginFromView(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                try:
                    user.groups.get()
                    login(request, user)
                    request.user = user
                    messages.success(request, "وارد شدید")
                    return redirect("website:main")

                except Group.DoesNotExist:
                    messages.warning(request, "گروهی برای شما تعیین نشده است")
                    return redirect("website:login")
            else:
                messages.warning(request, "نام کاربری یا رمز عبور صحیح نیست")
                return redirect("website:login")
            
    else:
        form=LoginForm()
        return render(request, "Login.html", {'form':form})
    
    return render(request, "Login.html", {"form":form})
    
    

def ProfessorProfile(request):
    username = User.objects.get(username=request.user.username)
    professor_name = username.professor
    p_university_list = professor_name.universities.all()

    context = {
        "professor":professor_name,
        "p_university":p_university_list,
    }
    return render(request, "professor/profile.html", context)



def ProfessorLessonList(request, p_code, u_code):
    professor_name = professor.objects.get(code=p_code)
    l_university = university.objects.get(code=u_code)
    lesson_list = professor_name.classes.all()

    context = {
        "list":lesson_list,
        "l_university":l_university,
    }
    
    return render(request, "professor/professor_lesson_list.html", context)



def LessonDetails(request, code):
    lesson_details = lesson.objects.get(code=code)
    return render(request, "lesson_details.html", {"lesson":lesson_details})
    


def GradeFormView(request):
    if request.method == "POST":
        form = GradeForm(request.POST)



def LessonSearchView(request):
    flag = False
    if request.method == "POST":
        flag = True
        form = LessonSearchForm(data=request.POST)
        if form.is_valid():

            # ? decides to use which model for searching
            if form.cleaned_data["query_lesson_code"] != None:
                result = lesson_class.objects.filter(Q(lesson_code=form.cleaned_data["query_lesson_code"]) &
                                                    Q(semester=form.cleaned_data["query_lesson_semester"]))
            else:
                if form.cleaned_data["query_lesson_name"] != "":
                    lessons = lesson.objects.filter(Q(name__contains=form.cleaned_data["query_lesson_name"]) |
                                                    Q(unit_type=form.cleaned_data["query_unit_type"]) |
                                                    Q(lesson_type=form.cleaned_data["query_lesson_type"]))
                else:
                    lessons = lesson.objects.filter(Q(unit_type=form.cleaned_data["query_unit_type"]) |
                                                    Q(lesson_type=form.cleaned_data["query_lesson_type"]))
                
                result = []
                temp = []
                for i in lessons:
                    temp.append(lesson_class.objects.filter(Q(lesson_code=i.code) &
                                                                Q(semester=form.cleaned_data["query_lesson_semester"])))
                for i in temp:
                    for j in range(0, len(i)):
                        result.append(i[j])
            
            context = {
                "result":result, 
                "form":form,
                "flag":flag
            }
            return render(request, "lesson_search_result.html", context)

    else:
        form = LessonSearchForm()
        return render(request, "lesson_search_result.html", {"form":form, "flag":flag})
    
    return render(request, "lesson_search_result.html", {"form":form, "flag":flag})

