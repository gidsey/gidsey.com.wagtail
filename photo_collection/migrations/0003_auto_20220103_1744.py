# Generated by Django 3.2.10 on 2022-01-03 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_collection', '0002_photocollection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photocollection',
            name='name',
        ),
        migrations.AlterField(
            model_name='photocollection',
            name='intro',
            field=models.CharField(max_length=250),
        ),
    ]
