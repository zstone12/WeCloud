from django.urls import path, include
from file.views import *

urlpatterns = [
    path('filedownload', FileDownload.as_view()),
    path('upfile', UpFile.as_view()),
    path('getfilebytime', GetFileByTime.as_view()),
    path('insertCoffer ', InsertCoffer.as_view()),
    path('restore', Restore.as_view()),
    path('delNote', delNote.as_view()),
    path('getList ', GetList.as_view()),
    path('insertNote', InsertNote.as_view()),
    path('getNote', GetNote.as_view()),
    path('deleteFile', DeleteFile.as_view()),
    path('gotoTrash', GotoTrash.as_view()),
    path('huifu', HuiFu.as_view())
]
