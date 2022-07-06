import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return '-' + ''.join(random.choice(chars) for _ in range(size))


def unique_slugify(instance, title):
    model = instance.__class__
    unique_slug = slugify(title)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slugify(title)
        unique_slug += random_string_generator(size=4)
    return unique_slug
