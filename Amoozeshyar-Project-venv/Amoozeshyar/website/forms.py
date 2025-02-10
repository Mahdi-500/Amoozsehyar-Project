from django import forms
from .models import student
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