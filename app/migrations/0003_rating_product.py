# Generated by Django 5.1 on 2024-08-11 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_rating_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='product',
            field=models.ForeignKey(default=4234, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
            preserve_default=False,
        ),
    ]
