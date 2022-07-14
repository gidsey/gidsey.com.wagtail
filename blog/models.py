from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.shortcuts import redirect
from django.shortcuts import render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail import images
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from base.blocks import (TitleAndTextBlock, SectionHeadBlock, ImageBlock, TwoImageBlock,
                         TwoThirdsOneThird, OneThirdTwoThirds)
from base.mixins import SocialMetaMixin
from .utils import paginate, get_tags


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(SocialMetaMixin, Page):
    """
    Blog detail page.
    """
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)

    hero = models.ForeignKey(
        images.get_image_model(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content = StreamField(
        [
            ('title_and_text', TitleAndTextBlock()),
            ('section_head', SectionHeadBlock()),
            ('image', ImageBlock()),
            ('two_images', TwoImageBlock()),
            ('two_thirds_one_third', TwoThirdsOneThird()),
            ('one_third_two_thirds', OneThirdTwoThirds()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def get_ordered_tags(self):
        """Specific ordered list of tags."""
        ordered_tags = self.tags.order_by('name')  # order by tag name
        return ordered_tags

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('date'),
                FieldPanel('tags'),
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('content'),
        FieldPanel('hero'),
        MultiFieldPanel(
            [
                InlinePanel('gallery_info', label='Gallery information', min_num=None, max_num=1),
                InlinePanel('gallery_images', label='Gallery images'),
            ],
            heading="Image Gallery"
        ),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label='Author', min_num=1, max_num=4),
            ],
            heading="Author(s)"
        )
    ]


class BlogIndexPage(RoutablePageMixin, Page):
    """
    Blog listing page.
    """

    template = 'blog/blog_index_page.html'
    max_count = 1

    intro = RichTextField(blank=True)

    social_image = models.ForeignKey(
        images.get_image_model(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='Add an image for social media meta data. Suggested size 1200 x 630px'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_posts = BlogPage.objects.live().public().order_by('-date')
        all_tags = [(tag.lower(), slug) for tag, slug in all_posts.values_list('tags__name', 'tags__slug')]
        all_tags = sorted(list(set(all_tags)))

        context, all_posts = get_tags(request, context, all_posts)
        posts = paginate(request, all_posts, 12)
        context['posts'] = posts
        context["categories"] = BlogCategory.objects.all()

        context['all_tags'] = all_tags
        context['location'] = self.url
        return context

    @route(r'^category/(?P<cat_slug>[-\w]*)/$', name="category_view")
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return redirect('/blog/')

        all_posts = BlogPage.objects.live().public().order_by('-date').filter(categories__in=[category])

        context, all_posts = get_tags(request, context, all_posts)
        posts = paginate(request, all_posts, 12)
        context['posts'] = posts
        context['category'] = category
        context['location'] = self.url + 'category/' + cat_slug
        return render(request, self.template, context)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('social_image'),
    ]


class BlogTagIndexPage(Page):
    """
    Tag index page.
    """

    max_count = 1

    def get_context(self, request, *args, **kwargs):
        # Filter by tag
        tag = request.GET.get('tag')
        posts = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['posts'] = posts
        return context


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["-name"]

    def __str__(self):
        return self.name


# noinspection PyUnresolvedReferences
@register_snippet
class BlogAuthor(models.Model):
    """
    Blog author for snippets.
    """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        images.get_image_model(),
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('image'),
            ],
            heading='Name and Image',
        ),
        MultiFieldPanel(
            [
                FieldPanel('website'),
            ],
            heading='Links',
        )
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'


class BlogPageAuthors(Orderable):
    """
    Select one or more blog authors.
    """
    page = ParentalKey(BlogPage, related_name='blog_authors', on_delete=models.CASCADE)
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)

    panel = [
        SnippetChooserPanel
    ]


class BlogPageGalleryImage(Orderable):
    """
    Select one or more images for blog pages.
    """
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    # noinspection PyUnresolvedReferences
    image = models.ForeignKey(
        images.get_image_model(), on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class BlogPageGalleryInfo(Orderable):
    """
    Holds the title and description for an in-page image gallery.
    """
    gallery_info = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_info')
    gallery_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Title')
    gallery_description = models.CharField(max_length=250, null=True, blank=True, verbose_name='Description')
