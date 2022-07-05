from django.db.models.signals import pre_save
from wagtail import images
from django.utils.text import slugify


def add_slug_to_image(instance, **kwargs):
    # print('add_slug called')
    # print(f'instance {instance}')
    instance.slug = slugify(instance.title)


def register_signal_handlers():
    # important: this function must be called at the app ready
    Image = images.get_image_model()
    pre_save.connect(add_slug_to_image, sender=Image)
