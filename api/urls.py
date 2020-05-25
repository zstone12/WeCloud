from django.contrib import admin
from django.urls import path
from django.urls import include
from api import views
urlpatterns = [
    path('test/',views.Test.as_view()),
    path('checkUsername',views.CheckUsername.as_view()),
    path('checkEmail',views.CheckEmail.as_view())
]