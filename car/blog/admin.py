from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(SignUp)
class SignUpAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'gender', 'joined']
    list_filter = ['gender', 'joined']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created']
    list_editable = ['status']
    list_filter = ['status', 'created', 'author']
    raw_id_fields = ['author']