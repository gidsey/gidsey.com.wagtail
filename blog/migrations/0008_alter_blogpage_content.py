# Generated by Django 3.2.9 on 2021-11-30 17:25

import base.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blogpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='add title', required=False)), ('text', base.blocks.SimpleRichTextBlock(help_text='add text', required=False))])), ('section_head', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='add section title', required=False))])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='add image', required=False)), ('hide_caption', wagtail.core.blocks.BooleanBlock(help_text='tick to hide caption', required=False)), ('alt_caption', wagtail.core.blocks.CharBlock(help_text='add custom caption (optional)', required=False))])), ('two_images', wagtail.core.blocks.StructBlock([('left_image', wagtail.images.blocks.ImageChooserBlock(help_text='add left-hand image', required=True)), ('right_image', wagtail.images.blocks.ImageChooserBlock(help_text='add right-hand image', required=True)), ('left_alt_caption', wagtail.core.blocks.CharBlock(help_text='add custom caption for left-hand image (optional)', required=False)), ('right_alt_caption', wagtail.core.blocks.CharBlock(help_text='add custom caption for right-hand image (optional)', required=False)), ('hide_captions', wagtail.core.blocks.BooleanBlock(help_text='tick to hide all captions', required=False))])), ('two_thirds_one_third', wagtail.core.blocks.StructBlock([('left_image', wagtail.images.blocks.ImageChooserBlock(help_text='add landscape left-hand image', required=True)), ('right_image', wagtail.images.blocks.ImageChooserBlock(help_text='add portrait right-hand image', required=True)), ('caption', wagtail.core.blocks.CharBlock(help_text='add a caption', required=False))])), ('one_third_two_thirds', wagtail.core.blocks.StructBlock([('left_image', wagtail.images.blocks.ImageChooserBlock(help_text='add portrait left-hand image', required=True)), ('right_image', wagtail.images.blocks.ImageChooserBlock(help_text='add landscape right-hand image', required=True)), ('caption', wagtail.core.blocks.CharBlock(help_text='add a caption', required=False))]))], blank=True, null=True),
        ),
    ]
