# Generated by Django 5.1 on 2024-08-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
