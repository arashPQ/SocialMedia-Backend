# Generated by Django 5.2 on 2025-05-11 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("-created_at",)},
        ),
    ]
