# Generated by Django 3.1.6 on 2021-03-25 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20210325_1000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpage',
            old_name='comments_toggle',
            new_name='comment_toggle',
        ),
    ]
