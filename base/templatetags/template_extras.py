from django import template

register = template.Library()


@register.filter
def social_url(img):
    return img.get_rendition('fill-1200x630|jpegquality-70').url


@register.filter
def original_url(img):
    return img.get_rendition('original').url
