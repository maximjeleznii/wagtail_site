# Generated by Django 3.1.7 on 2021-04-12 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20210324_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='email_link',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='google_link',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='twitter_link',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]