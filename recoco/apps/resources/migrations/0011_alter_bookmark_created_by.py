# Generated by Django 3.2.4 on 2021-07-06 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resources", "0010_alter_bookmark_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookmark",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookmarks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]