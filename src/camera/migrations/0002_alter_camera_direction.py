# Generated by Django 5.1.5 on 2025-01-22 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("camera", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="camera",
            name="direction",
            field=models.IntegerField(),
        ),
    ]
