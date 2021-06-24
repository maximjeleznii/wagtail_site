# Generated by Django 3.1.6 on 2021-03-24 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20210225_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogindexpage',
            name='intro',
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='hero_button',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='hero_headline',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='hero_text',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
