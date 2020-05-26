from django.db import models


# Create your models here.


class User(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    size = models.BigIntegerField(max_length=11, null=True)

    class Meta:
        db_table = "user"


class Img(models.Model):
    file_id = models.IntegerField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=11, null=False)

    class Meta:
        db_table = "img"


class Coffer:
    file_id = models.IntegerField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=11, null=False)

    class Meta:
        db_table = "coffer"


class Note:
    file_id = models.IntegerField(primary_key=True, null=False)
    title = models.CharField(max_length=255, null=True)
    content = models.CharField(max_length=255, null=True)
    date = models.DateField(max_length=20, null=True)
    display = models.IntegerField(max_length=11, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=11, null=False)

    class Meta:
        db_table = "note"


class Radio:
    file_id = models.IntegerField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=11, null=False)

    class Meta:
        db_table = "radio"


class Trash:
    file_id = models.IntegerField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=11, null=False)

    class Meta:
        db_table = "trash"


class Doc:
    file_id = models.IntegerField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=11, null=False)

    class Meta:
        db_table = "doc"
