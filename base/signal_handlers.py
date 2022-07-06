from django.db.models.signals import pre_save
from wagtail import images

from .utils import unique_slugify


def add_slug_to_image(instance, **kwargs):
    instance.slug = unique_slugify(instance, instance.title)


def register_signal_handlers():
    # initiated in wagtail_hooks
    pre_save.connect(add_slug_to_image, sender=images.get_image_model())
