# Generated by Django 4.0.5 on 2022-07-06 16:03

from django.db import migrations


def add_slugs_to_existing_images(apps, schema_editor):
    extended_image_model = apps.get_model('base', 'GidsImage')
    db_alias = schema_editor.connection.alias
    images = extended_image_model.objects.using(db_alias).all()
    for image in images:
        image.title = image.title
        image.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_gidsimage_slug_alter_socialmedia_favicon_and_more'),
    ]

    operations = [
        migrations.RunPython(add_slugs_to_existing_images)
    ]