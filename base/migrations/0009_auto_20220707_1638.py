# Generated by Django 4.0.6 on 2022-07-07 16:38

from django.core.management.color import no_style
from django.db import connection
from django.db import migrations


def sql_sequence_reset(apps, schema_editor):
    extended_image_model = apps.get_model('base', 'GidsImage')
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [extended_image_model])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0007_alter_gidsimage_slug_alter_socialmedia_favicon_and_more'),
    ]

    operations = [
        migrations.RunPython(sql_sequence_reset)
    ]
