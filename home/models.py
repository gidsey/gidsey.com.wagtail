from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from base import blocks


class HomePage(Page):
    max_count = 1
    home_title = models.CharField(max_length=250, null=True, blank=True)
    intro = RichTextField(blank=True)
    hero = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    content = StreamField(
        [
            ('preview_pane_block', blocks.PreviewPaneBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('home_title'),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('hero'),
        StreamFieldPanel('content'),
    ]


