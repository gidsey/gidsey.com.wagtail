from django.db.models.signals import pre_save
from django.utils.text import slugify
from wagtail import images

from .utils import random_string_generator


def add_slug_to_image(instance, **kwargs):
    try:
        instance.slug = slugify(instance.title)
    except Exception:
        instance.slug = slugify(instance.title) + '_' + random_string_generator(size=4)


def register_signal_handlers():
    # important: this function must be called at the app ready
    Image = images.get_image_model()
    pre_save.connect(add_slug_to_image, sender=Image)
