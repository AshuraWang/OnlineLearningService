# Generated by Django 4.0.4 on 2022-05-28 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='id',
        ),
        migrations.AlterField(
            model_name='prediction',
            name='request_id',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]
