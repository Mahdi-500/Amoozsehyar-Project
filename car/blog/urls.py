from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('CarBlog', views.Mainview, name="main"),
    path('CarBlog\SignUp', views.signupView, name="signup"),
    path('CarBlog\login', views.loginview, name='login'),
    path('CarBlog\<str:username>\createPost', views.AddPostview, name='add post'),
    path('CarBlog\<str:username>\profile', views.PostListview, name='profile'),
    path('CarBlog\<str:username>\post\<int:id>', views.PostDtailview, name='post detail')
]
