# Generated by Django 3.1.6 on 2021-03-26 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_blogpage_feed_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='chosen',
            field=models.BooleanField(default=False),
        ),
    ]
