from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


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
