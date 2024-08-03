from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('CarBlog\<str:username>\global', views.Mainview, name="main"),
    path('CarBlog', views.signupView, name="signup"),
    path('CarBlog\login', views.loginview, name='login'),
    path('CarBlog\<str:username>\createPost', views.AddPostview, name='add post'),
    path('CarBlog\<str:username>\profile', views.PostListview, name='profile'),
    path('CarBlog\<str:username>\post\<int:id>', views.PostDtailview, name='post detail'),
    path("CarBlog\Ticket", views.Ticketview, name='ticket'),
    path('CarBlog\<str:username>\global\post\<int:id>\comment', views.Commentview, name="comment"),
]
