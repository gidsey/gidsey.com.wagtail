from django.db import models
from wagtail import images
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page

from base.blocks import PhotoCollectionBlock
from base.mixins import SocialMetaMixin


class PhotoCollection(SocialMetaMixin, Page):
    """
    Photo collection detail page
    """
    intro = models.CharField(max_length=250, null=True, blank=True)
    hero = models.ForeignKey(
        images.get_image_model(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content = StreamField(
        [
            ('photo_collection_block', PhotoCollectionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('hero'),
        FieldPanel('content'),
    ]


class PhotoCollectionIndexPage(SocialMetaMixin, Page):
    """
    Photo Collection listing page.
    """

    template = 'photo_collection/photo_collection_index_page.html'
    max_count = 1

    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        collections = PhotoCollection.objects.live().public().order_by('title')
        context['collections'] = collections
        return context
