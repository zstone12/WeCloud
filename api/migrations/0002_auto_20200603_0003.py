# Generated by Django 2.0.9 on 2020-06-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='path',
            field=models.FileField(max_length=255, null=True, upload_to='doc/'),
        ),
        migrations.AlterField(
            model_name='img',
            name='path',
            field=models.FileField(max_length=255, null=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='path',
            field=models.FileField(max_length=255, null=True, upload_to='radio/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='path',
            field=models.FileField(max_length=255, null=True, upload_to='video/'),
        ),
    ]
