from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from api import models
from django.db import models


class Share(models.Model):
    share_id = models.IntegerField(primary_key=True, null=False)
    file_id = models.IntegerField()
    type = models.CharField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    share_no = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "share"
