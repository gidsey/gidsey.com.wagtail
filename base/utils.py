import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return '-' + ''.join(random.choice(chars) for _ in range(size))


def unique_slugify(instance):
    model = instance.__class__
    if instance.slug:
        return instance.slug

    origin = instance.title
    unique_slug = slugify(origin)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slugify(origin)
        unique_slug += random_string_generator(size=4)
    return unique_slug
