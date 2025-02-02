from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"
urlpatterns = [
    path('CarBlog/', views.Mainview, name="main"),

    # ? Authentication
    path('CarBlog/signup/', views.signupView, name="signup"),
    path('CarBlog/login/', views.loginview, name='login'),
    path("CarBlog/logout/", views.LogoutView, name="logout"),


    path('CarBlog/post/<int:id>/', views.PostDtailview, name='post detail'),
    path("CarBlog/Ticket/", views.Ticketview, name='ticket'),
    path('CarBlog/global/post/<int:id>/comment/', views.Commentview, name="comment"),
    path("CarBlog/search/", views.SearchView, name="search"),

    # ? user actions
    path('CarBlog/profile/', views.PostListview, name='profile'),
    path('CarBlog/createpost/', views.AddPostview, name='add post'),
    path('CarBlog/delete_post/<int:id>/', views.DeletePostView, name="delete post"),
    path('CarBlog/edit_post/<int:id>/', views.EditPostView, name='edit post'),
    
    # ? password change
    path('CarBlog/password_change/', auth_views.PasswordChangeView.as_view(success_url="done"), name='password change'),
    path('CarBlog/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password change done"),
]
