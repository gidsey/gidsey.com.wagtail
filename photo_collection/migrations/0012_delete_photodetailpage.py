# Generated by Django 4.0.6 on 2022-07-11 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_collection', '0011_alter_photocollection_fb_og_image_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhotoDetailPage',
        ),
    ]