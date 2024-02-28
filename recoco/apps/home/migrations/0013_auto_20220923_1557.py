# Generated by Django 3.2.15 on 2022-09-23 13:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("home", "0012_auto_20220923_1551"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="groupobjectpermissiononsite",
            unique_together={("group", "permission", "object_pk", "site")},
        ),
        migrations.AlterUniqueTogether(
            name="userobjectpermissiononsite",
            unique_together={("user", "permission", "object_pk", "site")},
        ),
    ]
