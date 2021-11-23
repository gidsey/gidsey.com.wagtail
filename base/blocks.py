from wagtail.core.blocks import StructBlock, RichTextBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock


class SimpleRichTextBlock(RichTextBlock):
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link',
            'ol',
            'ul',
        ]


class TitleAndTextBlock(StructBlock):
    """
    Title and text only.
    """
    title = CharBlock(required=False, help_text='add title')
    text = SimpleRichTextBlock(required=False, help_text='add text')

    class Meta:
        template = 'blog/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & Text'


class SectionHeadBlock(StructBlock):
    """
    Section head.
    """
    title = CharBlock(required=False, help_text='add section title')

    class Meta:
        template = 'blog/section_head.html'
        icon = 'edit'
        label = 'Section head'


class ImageBlock(StructBlock):
    """
    Image and caption.
    """
    image = ImageChooserBlock(required=False, help_text='add image')

    class Meta:
        template = 'blog/image_and_caption_block.html'
        icon = 'image'
        label = 'Image and caption'


class TwoImageBlock(StructBlock):
    """
    Two images side by side, each with caption.
    """
    left_image = ImageChooserBlock(required=True, help_text='add left-hand image')
    right_image = ImageChooserBlock(required=True, help_text='add right-hand image')

    class Meta:
        template = 'blog/two_image_block.html'
        icon = 'image'
        label = 'Two images with captions'


class TwoThirdsOneThird(StructBlock):
    """
    Two images arranged in a two-thirds / one-third column layout.
    Bespoke caption field.
    """
    left_image = ImageChooserBlock(required=True, help_text='add landscape left-hand image')
    right_image = ImageChooserBlock(required=True, help_text='add portrait right-hand image')
    caption = CharBlock(required=False, help_text='add section title')

    class Meta:
        template = 'blog/two_thirds_one_third_block.html'
        icon = 'image'
        label = 'Two images arranged in a two-thirds / one-third layout'


class OneThirdTwoThirds(StructBlock):
    """
    Two images arranged in a one-third / two-thirds column layout.
    Bespoke caption field.
    """
    left_image = ImageChooserBlock(required=True, help_text='add portrait left-hand image')
    right_image = ImageChooserBlock(required=True, help_text='add landscape right-hand image')
    caption = CharBlock(required=False, help_text='add section title')

    class Meta:
        template = 'blog/one_third_two_thirds_block.html'
        icon = 'image'
        label = 'Two images arranged in a one-third / two-thirds layout'
