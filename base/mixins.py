from django.db import models
from wagtail import images
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class SocialMetaMixin(models.Model):
    """
    Adds social media images to the Promote tab.

    Twitter summary card image.
    FB OG image.
    Alt tag text (used on both images).
    """

    class Meta:
        abstract = True

    twitter_card_image = models.ForeignKey(
        images.get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Suggested size: 1200px x 628px',
    )

    fb_og_image = models.ForeignKey(
        images.get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Facebook image',
        help_text='Suggested size: 1200px x 628px',
    )

    social_img_alt_text = models.CharField(
        max_length=100,
        help_text='Social image alt text - maximum 100 characters',
        null=True,
        blank=True
    )

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            ImageChooserPanel('twitter_card_image'),
            ImageChooserPanel('fb_og_image'),
            FieldPanel('social_img_alt_text'),
        ], heading='Social media Meta')
    ]
