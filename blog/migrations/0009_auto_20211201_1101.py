# Generated by Django 3.2.9 on 2021-12-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_blogpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpagegalleryimage',
            name='gallery_description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='blogpagegalleryimage',
            name='gallery_title',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
