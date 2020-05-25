
from django.db import models

# Create your models here.
class User(models.Model):

    user_id=models.IntegerField(primary_key=True,null=False)
    username=models.CharField(max_length=50,null=True)
    password=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True)
    size=models.BigIntegerField(max_length=11,null=True)
    class Meta:
        db_table = "user"

