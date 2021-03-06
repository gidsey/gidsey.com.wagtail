# Generated by Django 4.0.6 on 2022-07-14 15:00

import base.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_gidsimage_file_hash'),
        ('blog', '0018_alter_blogauthor_image_alter_blogpage_fb_og_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='social_image',
            field=models.ForeignKey(blank=True, help_text='Add an image for social media meta data. Suggested size 1200 x 630px', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.gidsimage'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='content',
            field=wagtail.fields.StreamField([('title_and_text', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='add title', required=False)), ('text', base.blocks.SimpleRichTextBlock(help_text='add text', required=False))])), ('section_head', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='add section title', required=False))])), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='add image', required=False)), ('hide_caption', wagtail.blocks.BooleanBlock(help_text='tick to hide caption', required=False)), ('alt_caption', wagtail.blocks.CharBlock(help_text='add custom caption (optional)', required=False))])), ('two_images', wagtail.blocks.StructBlock([('left_image', wagtail.images.blocks.ImageChooserBlock(help_text='add left-hand image', required=True)), ('right_image', wagtail.images.blocks.ImageChooserBlock(help_text='add right-hand image', required=True)), ('left_alt_caption', wagtail.blocks.CharBlock(help_text='add custom caption for left-hand image (optional)', required=False)), ('right_alt_caption', wagtail.blocks.CharBlock(help_text='add custom caption for right-hand image (optional)', required=False)), ('hide_captions', wagtail.blocks.BooleanBlock(help_text='tick to hide all captions', required=False))])), ('two_thirds_one_third', wagtail.blocks.StructBlock([('left_image', wagtail.images.blocks.ImageChooserBlock(help_text='add landscape left-hand image', required=True)), ('right_image', wagtail.images.blocks.ImageChooserBlock(help_text='add portrait right-hand image', required=True)), ('caption', wagtail.blocks.CharBlock(help_text='add a caption', required=False))])), ('one_third_two_thirds', wagtail.blocks.StructBlock([('left_image', wagtail.images.blocks.ImageChooserBlock(help_text='add portrait left-hand image', required=True)), ('right_image', wagtail.images.blocks.ImageChooserBlock(help_text='add landscape right-hand image', required=True)), ('caption', wagtail.blocks.CharBlock(help_text='add a caption', required=False))]))], blank=True, null=True, use_json_field=True),
        ),
    ]
