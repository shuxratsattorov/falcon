# Generated by Django 5.0.6 on 2024-08-07 07:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_productreview_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='username',
        ),
        migrations.AddField(
            model_name='productreview',
            name='username',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
