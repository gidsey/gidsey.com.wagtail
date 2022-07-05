from django.db.models.signals import pre_save
from django.utils.text import slugify
from wagtail import images

from .utils import random_string_generator


def unique_slugify(instance, title):
    model = instance.__class__
    print(f'model {model}')
    unique_slug = slugify(title)
    print(f'unique_slug 0 {unique_slug}')
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slugify(title)
        print(f'unique_slug 1 {unique_slug}')
        unique_slug += random_string_generator(size=4)
        print(f'unique_slug 2 {unique_slug}')
    print(f'unique_slug 3 {unique_slug}')
    return unique_slug


def add_slug_to_image(instance, **kwargs):
    print('add_slug_to_image called')
    print(f'instance = {instance}')

    instance.slug = unique_slugify(instance, instance.title)


def register_signal_handlers():
    # important: this function must be called at the app ready
    Image = images.get_image_model()
    pre_save.connect(add_slug_to_image, sender=Image)
