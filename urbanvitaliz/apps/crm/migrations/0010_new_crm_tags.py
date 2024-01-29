# Generated by Django 3.2.23 on 2024-01-23 17:10

from django.db import migrations


def reverse_historical_tags(apps, schema_editor):
    Tag = apps.get_model("taggit", "Tag")
    for slug in ["diag", "edl", "contact", "general"]:
        try:
            tag = Tag.objects.get(slug=f"crm_{slug}")
            tag.name = slug
            tag.save()
        except Tag.DoesNotExist:
            pass


def update_historical_tags(apps, schema_editor):
    Tag = apps.get_model("taggit", "Tag")

    default_tags = [
        ("diag", "Diagnostic"),
        ("edl", "État des lieux"),
        ("contact", "Mise en relation"),
        ("general", "Général positif"),
    ]

    # update tags name
    for slug, name in default_tags:
        try:
            tag = Tag.objects.get(slug=slug)
            tag.slug = f"crm_{tag.slug}"
            tag.name = name
            tag.save()
        except Tag.DoesNotExist:
            pass


def _get_tag_mapping(apps):
    Tag = apps.get_model("taggit", "Tag")

    return {
        "crm_diag": Tag.objects.filter(name__iexact="Diagnostic").first(),
        "crm_edl": Tag.objects.filter(name__iexact="État des lieux").first(),
        "crm_contact": Tag.objects.filter(name__iexact="Mise en relation").first(),
        "crm_general": Tag.objects.filter(name__iexact="Général positif").first(),
    }


class Migration(migrations.Migration):
    def assign_new_tags(apps, schema_editor):
        TaggedItem = apps.get_model("taggit", "TaggedItem")

        tag_mapping = _get_tag_mapping(apps)

        for slug, tag in tag_mapping.items():
            if tag:
                TaggedItem.objects.filter(tag__slug=slug).update(tag=tag)

    def assign_old_tags(apps, schema_editor):
        Tag = apps.get_model("taggit", "Tag")
        TaggedItem = apps.get_model("taggit", "TaggedItem")

        tag_mapping = _get_tag_mapping(apps)

        for slug, tag in tag_mapping.items():
            if tag:
                old_tag = Tag.objects.get(slug=slug)
                TaggedItem.objects.filter(tag=tag).update(tag=old_tag)

    dependencies = [
        ("crm", "0009_project_annotations"),
    ]

    operations = [
        migrations.RunPython(update_historical_tags, reverse_historical_tags),
        migrations.RunPython(assign_new_tags, assign_old_tags),
    ]
