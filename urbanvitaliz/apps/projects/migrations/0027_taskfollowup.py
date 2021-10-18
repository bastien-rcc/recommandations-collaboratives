# Generated by Django 3.2.8 on 2021-10-18 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0026_alter_project_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskFollowup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "en cours"),
                            (2, "blocage"),
                            (3, "terminé"),
                            (4, "refusé"),
                        ]
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("comment", models.TextField(blank=True, default="")),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followups",
                        to="projects.task",
                    ),
                ),
                (
                    "who",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_followups",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "suivi action",
                "verbose_name_plural": "suivis actions",
            },
        ),
    ]
