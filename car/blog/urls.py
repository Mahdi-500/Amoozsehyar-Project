from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.signupView, name="signup"),
    path('\login', views.loginview, name='login'),
    path('\<str:username>\createPost', views.AddPostview, name='add post'),
    path('\<str:username>\profile', views.PostListview, name='profile'),
    path('\<str:username>\post\<int:id>', views.PostDtailview, name='post detail')
]
