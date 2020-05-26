from django.contrib import admin

# Register your models here.
from api import models

admin.register(models.User)
admin.register(models.Video)
admin.register(models.Coffer)
admin.register(models.Trash)
admin.register(models.Radio)
admin.register(models.Note)
admin.register(models.Doc)
admin.register(models.Img)