from .models import SignUp, Login, Post, Ticket, Comment
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


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["name", "email", "title", "message", "type"]

    def clean(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']

        if not str(name).isalpha():
            raise forms.ValidationError("name must be letters only")
        
        if "@" not in str(email):
            raise forms.ValidationError("invalid email")
        
        if str(email)[str(email).find("@") + 1:] != "gmail.com" and str(email)[str(email).find("@") + 1:] != "yahoo.com":
            raise forms.ValidationError("must be a gmail or a yahoo mail")
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']