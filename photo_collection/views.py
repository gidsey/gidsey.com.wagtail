from django.http import Http404
from django.views.generic import TemplateView
from wagtail import images
from wagtail.images.models import SourceImageIOError


class PhotoDetailPage(TemplateView):
    template_name = 'photo_collection/photo_detail_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PhotoDetailPage, self).get_context_data(**kwargs)
        image_id = self.kwargs.get('id')
        try:
            image = images.get_image_model().objects.get(id=image_id)
            context['image'] = image
            context['rendition'] = image.get_rendition('width-2400|jpegquality-80').url
            return context
        except SourceImageIOError:
            raise Http404
