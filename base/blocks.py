from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class SimpleRichTextBlock(blocks.RichTextBlock):
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link',
            'ol',
            'ul',
        ]


class TitleAndTextBlock(blocks.StructBlock):
    """
    Title and text only.
    """
    title = blocks.CharBlock(required=False, help_text='add title')
    text = SimpleRichTextBlock(required=False, help_text='add text')

    class Meta:
        template = 'blog/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & Text'


class SectionHeadBlock(blocks.StructBlock):
    """
    Section head.
    """
    title = blocks.CharBlock(required=False, help_text='add section title')

    class Meta:
        template = 'blog/section_head.html'
        icon = 'edit'
        label = 'Section head'


class ImageBlock(blocks.StructBlock):
    """
    Image and caption.
    """
    image = ImageChooserBlock(required=False, help_text='add image')

    class Meta:
        template = 'blog/image_and_caption_block.html'
        icon = 'image'
        label = 'Image and caption'


class TwoImageBlock(blocks.StructBlock):
    """
    Two images side by side, each with caption.
    """

    left_image = ImageChooserBlock(required=False, help_text='add left-hand image')
    right_image = ImageChooserBlock(required=False, help_text='add right-hand image')

    class Meta:
        template = 'blog/two_image_block.html'
        icon = 'image'
        label = 'Two images with captions'


