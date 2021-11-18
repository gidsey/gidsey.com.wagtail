from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, ObjectList, TabbedInterface, FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting(icon='mail')
class SocialMedia(BaseSetting):
    site_name = models.CharField(max_length=255, null=True, blank=True,
                                 help_text='Webiste name')
    email = models.EmailField(null=True, blank=True,
                              help_text='Your email address')
    twitter = models.CharField(max_length=255, null=True, blank=True,
                               help_text='Your Twitter username, without the @')
    instagram = models.CharField(max_length=255, null=True, blank=True,
                                 help_text='Your Instagram username, without the @')
    flickr = models.URLField(null=True, blank=True,
                             help_text='Your Flickr homepage URL')
    glass = models.URLField(null=True, blank=True,
                            help_text='Your Glass profile page URL')

    site_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('favicon'),
                ImageChooserPanel('site_icon'),
            ],
            heading="Images",
        ),

        MultiFieldPanel(
            [FieldPanel('site_name')],
            heading="Site Name",
        ),

        MultiFieldPanel(
            [FieldPanel('email')],
            heading="Email",
        ),

        MultiFieldPanel(
            [FieldPanel('twitter')],
            heading="Twitter",
        ),

        MultiFieldPanel(
            [FieldPanel('flickr')],
            heading="Flickr",
        ),

        MultiFieldPanel(
            [FieldPanel('instagram')],
            heading="Instagram",
        ),

        MultiFieldPanel(
            [FieldPanel('glass')],
            heading="Glass",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Social Media"),
    ])
