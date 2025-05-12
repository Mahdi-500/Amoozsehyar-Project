from django import forms
from django_jalali.db import models as jmodels
from .models import student, professor, lesson, lesson_class, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = student
        fields = "__all__"
        exclude = ["created", "modified", "role", "user", "last_year", "student_number"]

        help_texts = {
            "mobile": "مثال: 09121234567",
            "date_of_birth":"مثال: 25-08-1357",
        }

        widget = {
            "date_of_birth":forms.TextInput(attrs={
                "dir":"rtl"})
        }

    def clean(self):
        clean_data = super().clean()
        first_name = clean_data.get("first_name")
        last_name = clean_data.get("last_name")
        student_id = clean_data.get("student_id")
        
        space_fname = first_name.find(" ")
        space_lname = last_name.find(" ")

        # ? first name validation
        if space_fname != -1:
            first_name = first_name.split(' ')
            for i in first_name:
                if not i.isalpha():
                    raise forms.ValidationError("فقط حروف الفبا در نام و نام خانوادگی مجاز است")
        else:
            if not first_name.isalpha():
                raise forms.ValidationError("فقط حروف الفبا در نام و نام خانوادگی مجاز است")
            

        # ? last name validation
        if space_lname != -1:
            last_name = last_name.split(' ')
            for i in last_name:
                if not i.isalpha():
                    raise forms.ValidationError("فقط حروف الفبا در نام و نام خانوادگی مجاز است")
        else:
            if not last_name.isalpha():
                raise forms.ValidationError("فقط حروف الفبا در نام و نام خانوادگی مجاز است")
        
        if not student_id.isdigit():
            raise forms.ValidationError("فقط عدد مجاز است")
        
        if len(student_id) < 10:
            raise forms.ValidationError("کد ملی باید 10 کاراکتر باشد")
        

class ProfessorForm(forms.ModelForm):

    class Meta:
        model = professor
        fields = "__all__"
        exclude = ['created', 'modified', 'role', 'user', 'code']

        widgets = {
            "universities": forms.CheckboxSelectMultiple,
            "date_of_birth":forms.TextInput(attrs={
                "dir":"rtl"})
        }

        help_texts = {
            "phone":"مثال: 09121234567",
            "date_of_birth": "مثال: 25-12-1357",
        }

    def clean(self):
        clean_data = super().clean()
        first_name = clean_data.get("first_name")
        last_name = clean_data.get("last_name")
        major = clean_data.get("professor_major")
        professor_id = clean_data.get("professor_id")

        student_object = student.objects.all().filter(student_id=professor_id)

        if student_object:
            raise forms.ValidationError("کد ملی را با دقت وارد کنید")
        
        if not first_name.isalpha() or not last_name.isalpha():
            raise forms.ValidationError("فقط حروف الفبا مجاز است")
        
        major = major.split(' ')
        for i in major:
            if not i.isalpha():
                raise forms.ValidationError("فقط حروف الفبا مجاز است")
        
        if not professor_id.isdigit():
            raise forms.ValidationError("فقط عدد مجاز است")
        
        if len(professor_id) < 10:
            raise forms.ValidationError("کد ملی باید 10 کاراکتر باشد")
        

    # def save(self, commit=True):
    #     professor = super().save(commit=False)
    #     if commit:
    #         professor.save()
    #         # ? Save the many-to-many data
    #         self.save_m2m()
    #     return professor



class LessonForm(forms.ModelForm):
    class Meta:
        model = lesson
        fields = [
            "name", "unit", "unit_type", "lesson_type",
            "pishniaz", "hamniaz", "lesson_major"
        ]

        widgets = {
            "pishniaz": forms.CheckboxSelectMultiple,
            "hamniaz": forms.CheckboxSelectMultiple,
            "lesson_major":forms.CheckboxSelectMultiple
        }

    def clean(self):
        clean_data = super().clean()
        name = clean_data.get("name")

        for name in name.split(" "):
            if not name.isalpha() and not name.isalnum():
                raise forms.ValidationError(" ترکیب عدد با حروف الفبا یا فقط حروف الفبا مجاز است")
            
            

class LessonClassFrom(forms.ModelForm):
    class Meta:
        model = lesson_class
        fields = "__all__"
        exclude = ['created', 'modified']

        help_texts = {
            "lesson_time":"مثال: 09:05 تا 15:00"
        }

        widgets = {
            "lesson_time":forms.TextInput(attrs={
                "dir":"rtl"
            })
        }

    def clean(self):
        clean_date = super().clean()
        time = clean_date.get("lesson_time")
        index = [i for i,x in enumerate(time) if x == ":"]
        temp = time.find("تا")

        # ? saving the numbers
        first_time_hour = time[:index[0]]
        first_time_minute = time[index[0] + 1:index[0] + 3]
        second_time_hour = time[index[1] - 2:index[1]]
        second_time_minute = time[index[1] + 1:]
        
        if len(index) != 2:
            raise forms.ValidationError("فرمت وارد شده صحیح نیست")
        
        if temp < 0:
            raise forms.ValidationError("کلمه ' تا ' حتما باید درج شود")
        
        if temp != 5 and temp != 6:
            raise forms.ValidationError("کلمه ' تا ' را براساس فرمت داده شده در جای مناسب قرار دهید")
        
        if not first_time_hour.isdigit() or not first_time_minute.isdigit() or not second_time_hour.isdigit() or not second_time_minute.isdigit():
            raise forms.ValidationError("فرمت وارد شده صحیح نیست")
        
        if (int(first_time_hour) > 24 or int(first_time_hour) < 1) or (int(second_time_hour) > 24 or int(second_time_hour) < 1):
            raise forms.ValidationError("مقدار ساعت باید بین 1 تا 24 باشد")
        
        if (int(first_time_minute) > 59 or int(first_time_minute) < 0) or (int(second_time_minute) > 59 or int(second_time_minute) < 0):
            raise forms.ValidationError("مقدار دقیقه باید بین 1 تا 59 باشید")
        


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = "__all__"
        exclude = ['created', 'modified']

    
    def clean(self):
        clean_data = super().clean()
        score = clean_data.get["score"]

        if 0 > score > 20:
            raise forms.ValidationError("نمره باید بین 0 تا 20 باشد")
        


class LoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور", required=True)



LESSON_TYPE_CHOICES = [("", "----------------"), 
                    ("اصلی", "اصلی"),
                    ("پایه", "پایه"),
                    ("عمومی", "عمومی"),
                    ("تخصصی", "تخصصی"),
                    ("اختیاری", "اختیاری")]

UNIT_TYPE_CHOICES = [("", "----------------"),
                    ("نظری", "نظری"),
                    ("نظری-عملی", "نظری - عملی"),
                    ("عملی", "عملی"),
                    ("آز", "آزمایشگاهی"),
                    ("کارآموزی", "کارآموزی")]
class LessonSearchForm(forms.Form):
    
    today_date_month = jmodels.jdatetime.date.today().month
    today_date_year = str(jmodels.jdatetime.date.today().year)
    
    if 11 <= today_date_month <= 12:
        today_date_year[1:] += '2'
        
    elif 1 <= today_date_month <= 3:
        year = str(int(today_date_year) - 1)[1:]
        today_date_year = year + "2"

    elif 6 <= today_date_month <= 10:
        today_date_year[1:] += "1"

    query_lesson_code = forms.IntegerField(label="کد درس", required=False)
    query_lesson_name = forms.CharField(label="نام درس", required=False)
    query_lesson_semester= forms.CharField(label="نیمسال", initial= today_date_year, required=True)
    #query_lesson_location = forms.CharField(label="")
    query_unit_type = forms.ChoiceField(choices=UNIT_TYPE_CHOICES, label="نوع واحد", required=False)
    query_lesson_type = forms.ChoiceField(choices=LESSON_TYPE_CHOICES, label="نوع درس", required=False)