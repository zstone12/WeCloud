from django.contrib import admin
from django.urls import path
from django.urls import include
from api import views
urlpatterns = [
    path('test/',views.Test.as_view()),
    path('checkUsername',views.CheckUsername.as_view()),
    path('checkEmail',views.CheckEmail.as_view()),
    path('reg',views.Reg.as_view()),
    path('login',views.Login.as_view()),
    path('isLog',views.IsLog.as_view()),
    path('cheakPassword',views.CheckPassword.as_view()),
    path('outLogin',views.OutLogin.as_view())

]