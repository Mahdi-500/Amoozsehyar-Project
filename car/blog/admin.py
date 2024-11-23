from django.contrib import admin
from .models import *

# Register your models here.

# ? Inlines
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


# ? admin actions
@admin.action(description="mark all selected items as Accepted")
def make_accept(modeladmin, request, queryset):
    queryset.update(status="AC")


# ? admin classes
@admin.register(SignUp)
class SignUpAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'gender', 'joined']
    list_filter = ['gender', 'joined']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", 'title', 'author', 'status', 'created', 'reading_time']
    list_editable = ['status', "reading_time"]
    list_filter = ['status', 'created', 'author']
    raw_id_fields = ['author']
    prepopulated_fields = {"slug": ["title"]}
    actions = [make_accept]
    inlines = [ImageInline, CommentInline]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'type', 'created']
    list_filter = ['type', 'created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'status']
    list_editable = ['status']
    list_filter = ['created', 'status']
    actions = [make_accept]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id","__str__", "date_created"]
    list_filter = ['date_created']
