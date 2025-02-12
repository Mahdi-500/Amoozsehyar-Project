from django import forms
from django_select2 import forms as s2forms
from .models import student, professor, university
from django_jalali import forms as jform

class StudentForm(forms.ModelForm):
    class Meta:
        model = student
        fields = [
            "first_name", "last_name", "student_id", "date_of_birth",
            "photo", "marriage", "mobile", "address", "gender", "university", "major"
        ]

        help_texts = {
            "mobile": "مثال: 09121234567",
            "date_of_birth":"مثال: 01-01-1357",
        }

    def clean(self):
        clean_data = super().clean()
        first_name = clean_data.get("first_name")
        last_name = clean_data.get("last_name")
        student_id = clean_data.get("student_id")
        
        if not first_name.isalpha() and not last_name.isalpha():
            raise forms.ValidationError("فقط حروف الفبا مجاز است")
        
        if not student_id.isdigit():
            raise forms.ValidationError("فقط عدد مجاز است")
        
        if len(student_id) < 10:
            raise forms.ValidationError("کد ملی باید 10 کاراکتر باشد")
        

class ProfessorForm(forms.ModelForm):
    # universities = forms.ModelMultipleChoiceField(
    #     queryset= university.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
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
            "date_of_birth": "مثال: 01-01-1357",
        }

    def clean(self):
        clean_data = super().clean()
        first_name = clean_data.get("first_name")
        last_name = clean_data.get("last_name")
        major = clean_data.get("professor_major")
        professor_id = clean_data.get("professor_id")

        if not first_name.isalpha() and not last_name.isalpha() and not major.isalpha():
            raise forms.ValidationError("فقط حروف الفبا مجاز است")
        
        if not professor_id.isdigit():
            raise forms.ValidationError("فقط عدد مجاز است")
        
        if len(professor_id) < 10:
            raise forms.ValidationError("کد ملی باید 10 کاراکتر باشد")
        

    def save(self, commit=True):
        professor = super().save(commit=False)
        if commit:
            professor.save()
            # ? Save the many-to-many data
            self.save_m2m()
        return professor