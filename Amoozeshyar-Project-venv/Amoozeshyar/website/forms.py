from django import forms
from .models import student, professor, lesson, lesson_class

class StudentForm(forms.ModelForm):
    class Meta:
        model = student
        fields = [
            "first_name", "last_name", "student_id", "date_of_birth",
            "photo", "marriage", "mobile", "address", "gender", "university", "major"
        ]

        help_texts = {
            "mobile": "مثال: 09121234567",
            "date_of_birth":"مثال: 25-12-1357",
        }

    def clean(self):
        clean_data = super().clean()
        first_name = clean_data.get("first_name")
        last_name = clean_data.get("last_name")
        student_id = clean_data.get("student_id")
        
        first_name = first_name.split(' ')
        last_name = last_name.split(' ')
        for i, j in first_name, last_name:
            if not i.isalpha() or not j.isalpha():
                raise forms.ValidationError("فقط حروف الفبا مجاز است")
        
        if not student_id.isdigit():
            raise forms.ValidationError("فقط عدد مجاز است")
        
        if len(student_id) < 10:
            raise forms.ValidationError("کد ملی باید 10 کاراکتر باشد")
        

class ProfessorForm(forms.ModelForm):

    class Meta:
        model = professor
        fields = [
            "first_name", "last_name", "date_of_birth",
            "professor_id", "photo", "professor_major",
            "email", "phone", "universities"
        ]

        widgets = {
            "universities": forms.CheckboxSelectMultiple
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
            if not name.isalpha() or not name.isalnum():
                raise forms.ValidationError(" ترکیب عدد با حروف الفبا یا فقط حروف الفبا مجاز است")
            

class LessonClassFrom(forms.ModelForm):
    class Meta:
        model = lesson_class
        fields = "__all__"
        exclude = ['created', 'modified']

        help_texts = {
            "lesson_time":"مثال: 09:30 تا 15:05"
        }

        widgets = {
            "lesson_time":forms.TextInput(attrs={
                "dir":"rtl"
            })
        }


    def clean(self):
        clean_date = super().clean()
        time = clean_date.get("lesson_time")
        day = clean_date.get("lesson_day")
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
        
        if temp != 5:
            raise forms.ValidationError("کلمه ' تا ' را براساس فرمت داده شده در جای مناسب قرار دهید")
        
        if not first_time_hour.isdigit() or not first_time_minute.isdigit() or not second_time_hour.isdigit() or not second_time_minute.isdigit():
            raise forms.ValidationError("فرمت وارد شده صحیح نیست")
        
        if 1 > int(first_time_hour) > 24 or 1 > int(second_time_hour) > 24:
            raise forms.ValidationError("مقدار ساعت باید بین 1 تا 24 باشد")
        
        if 1 > int(first_time_minute) > 59 or 1 > int(second_time_minute) > 59:
            raise forms.ValidationError("مقدار دقیقه باید بین 1 تا 59 باشید")