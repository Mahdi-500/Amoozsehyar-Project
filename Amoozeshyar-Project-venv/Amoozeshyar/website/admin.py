from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'entrance_year', 'last_year']
    raw_id_fields = ["major", "university", "user"]

@admin.register(major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "capacity"]
    list_editable = ["capacity"]

@admin.register(university)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

@admin.register(professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    raw_id_fields = ["universities"]