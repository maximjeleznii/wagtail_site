# Generated by Django 3.1.6 on 2021-02-22 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210222_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactinfo',
            name='name',
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='message',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
