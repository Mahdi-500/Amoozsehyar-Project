from .models import SignUp, Login, Post
from django import forms

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['name', 'username', 'password', 'gender']

    def clean(self):
        name = self.cleaned_data['name']
        password = self.cleaned_data["password"]

        if not str(name).isalpha():
            raise forms.ValidationError("name must be letters only")
        
        elif not str(password).isalnum():
            raise forms.ValidationError("password must be combination of letters and numbers")
        
        elif len(password) < 8:
            raise forms.ValidationError("password must be at least 8 characters")


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password']

class PostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "engine_type"]