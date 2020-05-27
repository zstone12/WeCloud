from django.contrib import admin
from django.urls import path
from django.urls import include
from sharefile import views

urlpatterns = [
    path('test', views.Test.as_view()),
    path('ShareToFile', views.ShareToFile.as_view()),
    path('ShareShowFile', views.ShareShowFile.as_view()),
    path('ShareSaveFile', views.ShareSaveFile.as_view()),
]