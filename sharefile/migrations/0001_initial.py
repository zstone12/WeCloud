# Generated by Django 2.0.9 on 2020-05-31 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('share_id', models.IntegerField(primary_key=True, serialize=False)),
                ('file_id', models.IntegerField()),
                ('type', models.CharField(max_length=20, null=True)),
                ('path', models.CharField(max_length=255, null=True)),
                ('share_no', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'share',
            },
        ),
    ]
