from django.db import models
from django.shortcuts import get_object_or_404
from wagtail import images
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from base.blocks import PhotoCollectionBlock
from base.mixins import SocialMetaMixin


class PhotoCollection(SocialMetaMixin, Page):
    """
    Photo collection detail page
    """
    intro = models.CharField(max_length=250, null=True, blank=True)
    # noinspection PyUnresolvedReferences
    hero = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content = StreamField(
        [
            ('photo_collection_block', PhotoCollectionBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('hero'),
        StreamFieldPanel('content'),
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


class PhotoDetailPage(RoutablePageMixin, Page):
    """
    Single photo detail page
    """

    template = 'photo_collection/photo_detail_page.html'
    max_count = 1

    @route(r'^photo/(\d+)/$', name='single_photo')
    def single_photo(self, request, photo=None):
        Image = images.get_image_model()
        image = get_object_or_404(Image, id=photo)
        return self.render(request, context_overrides={
            'image': image,
        })
