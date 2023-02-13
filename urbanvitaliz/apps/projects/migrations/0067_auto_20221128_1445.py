# Generated by Django 3.2.16 on 2022-11-28 13:45

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import urbanvitaliz.apps.projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('projects', '0066_alter_project_status'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='document',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', urbanvitaliz.apps.projects.models.DocumentOnSiteManager()),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.site'),
            preserve_default=False,
        ),
    ]