# Generated by Django 5.1.5 on 2025-01-22 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plant", "0002_plant_layout"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="layout",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
