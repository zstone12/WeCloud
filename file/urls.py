from django.urls import path, include
from file.views import *
from api.views import *

urlpatterns = [
    path('filedownload', FileDownload.as_view()),
    path('upfile', UpFile.as_view()),
    path('getfilebytime', GetFileByTime.as_view()),
    path('insertcoffer', InsertCoffer.as_view()),
    path('createnote',CreateNote.as_view()),
    path('getlist', GetList.as_view()),
    path('restore', Restore.as_view()),
    path('delnote', delNote.as_view()),
    path('updatenote', UpdateNote.as_view()),
    path('getnote', GetNote.as_view()),
    path('deletefile', DeleteFile.as_view()),
    path('gototrash', GotoTrash.as_view()),
    path('huifu', HuiFu.as_view()),
    path('getfile', GetFile.as_view()),
]
