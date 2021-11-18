from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class SimpleRichTextBlock(blocks.RichTextBlock):
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link'
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


class ImageBlock(blocks.StructBlock):
    """
    Image and caption.
    """
    image = ImageChooserBlock(required=False, help_text='add image')

    class Meta:
        template = 'blog/image_and_caption_block.html'
        icon = 'image'
        label = 'Image and caption'
