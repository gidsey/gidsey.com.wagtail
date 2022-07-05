# Generated by Django 4.0.5 on 2022-07-05 14:51

from django.db import migrations


def add_slugs_to_existing_images(apps, schema_editor):
    extended_image_model = apps.get_model('base', 'GidsImage')
    db_alias = schema_editor.connection.alias
    images = extended_image_model.objects.using(db_alias).all()
    for image in images:
        image.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20220705_1425'),
    ]

    operations = [
        migrations.RunPython(add_slugs_to_existing_images)
    ]
