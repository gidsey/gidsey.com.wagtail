# Generated by Django 4.0.3 on 2022-04-07 17:32

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_homepage_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='body',
            new_name='intro',
        ),
        migrations.AddField(
            model_name='homepage',
            name='home_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([('preview_pane_block', wagtail.core.blocks.StructBlock([('preview_image', wagtail.images.blocks.ImageChooserBlock(help_text='add a square image here', required=True)), ('destination', wagtail.core.blocks.PageChooserBlock(help_text='choose the page to link to', required=True))]))], blank=True, null=True),
        ),
    ]
