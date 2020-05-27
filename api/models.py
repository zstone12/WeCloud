from django.db import models


# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    size = models.BigIntegerField(max_length=11, null=True)

    class Meta:
        db_table = "user"


class Img(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "img"


class Coffer(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "coffer"


class Note(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=255, null=True)
    content = models.CharField(max_length=255, null=True)
    date = models.DateField(max_length=20, null=True)

    display = models.IntegerField(max_length=11, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "note"


class Radio(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "radio"


class Trash(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "trash"


class Doc(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "doc"


class Video(models.Model):
    file_id = models.AutoField(primary_key=True, null=False)
    filename = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, null=True)
    size = models.BigIntegerField(max_length=11, null=True)
    date = models.DateField(max_length=20, null=True)
    path = models.CharField(max_length=255, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "video"


