from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from wagtail import images
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from base import blocks


class PhotoCollection(Page):
    """
    Photo collection detail page
    """
    intro = models.CharField(max_length=250, null=True, blank=True)
    hero = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content = StreamField(
        [
            ('photo_collection_block', blocks.PhotoCollectionBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('hero'),
        StreamFieldPanel('content'),
    ]


class PhotoCollectionIndexPage(Page):
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
        try:
            image = images.get_image_model().objects.get(id=photo)
            # print(f'image {image}')
            return self.render(request, context_overrides={
                'image': image,
                'rendition': image.get_rendition('width-2000|jpegquality-80').url,
            })
        except ObjectDoesNotExist:
            raise Http404
