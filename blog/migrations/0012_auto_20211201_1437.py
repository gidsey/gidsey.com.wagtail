# Generated by Django 3.2.9 on 2021-12-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blogpagegalleryinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpagegalleryinfo',
            name='gallery_description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='blogpagegalleryinfo',
            name='gallery_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Title'),
        ),
    ]
