# Generated by Django 5.2 on 2025-06-22 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notification", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="type_of_notification",
            field=models.CharField(
                choices=[
                    ("postcomment", "Post comment"),
                    ("postlike", "Post like"),
                    ("acceptedfollowrequest", "Accepted followrequest"),
                    ("rejectedfollowrequest", "Rejected followrequest"),
                    ("newfollowrequest", "New followrequest"),
                ],
                max_length=50,
            ),
        ),
    ]
