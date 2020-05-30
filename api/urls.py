from django.contrib import admin
from django.urls import path
from django.urls import include
from api import views
urlpatterns = [
    path('test/',views.Test.as_view()),
    path('users/checkUsername',views.CheckUsername.as_view()),
    path('users/checkEmail',views.CheckEmail.as_view()),
    path('users/reg',views.Reg.as_view()),
    path('users/login',views.Login.as_view()),
    path('users/isLog',views.IsLog.as_view()),
    path('users/cheakPassword',views.CheckPassword.as_view()),
    path('users/outLogin',views.OutLogin.as_view()),
    path('getFile',views.GetFile.as_view())

]
