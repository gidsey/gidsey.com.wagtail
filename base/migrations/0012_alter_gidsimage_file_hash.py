# Generated by Django 4.0.6 on 2022-07-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_gidsimage_copyright'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gidsimage',
            name='file_hash',
            field=models.CharField(blank=True, db_index=True, editable=False, max_length=40),
        ),
    ]
