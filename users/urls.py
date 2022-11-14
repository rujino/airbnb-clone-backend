from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path(
        "@<str:username>", views.PublicUsers.as_view()
    ),  # @붙이는 이유: me라는 유저가 있을 수 도 있잖아
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
]
