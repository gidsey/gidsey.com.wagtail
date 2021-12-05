from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render

from base import blocks


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    """
    Blog detail page.
    """
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    hero = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('section_head', blocks.SectionHeadBlock()),
            ('image', blocks.ImageBlock()),
            ('two_images', blocks.TwoImageBlock()),
            ('two_thirds_one_third', blocks.TwoThirdsOneThird()),
            ('one_third_two_thirds', blocks.OneThirdTwoThirds()),
        ],
        null=True,
        blank=True
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
        StreamFieldPanel('content'),
        ImageChooserPanel('hero'),
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_posts = BlogPage.objects.live().public().order_by('-date')
        all_tags = [(tag.lower(), slug) for tag, slug in all_posts.values_list('tags__name', 'tags__slug')]
        all_tags = sorted(list(set(all_tags)))

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])

        # Paginate all posts
        paginator = Paginator(all_posts, 12)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['all_tags'] = all_tags
        context['num_posts'] = paginator.count
        context["categories"] = BlogCategory.objects.all()
        return context

    @route(r'^tagged/(\w+)/$')
    def index_by_tag(self, request, tag):
        blogpages = BlogPage.objects.filter(tags__name=tag)

        return render(request, 'blog/index_by_tag.html', {
            'page': self,
            'blogpages': blogpages
        })

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
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
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


@register_snippet
class BlogAuthor(models.Model):
    """
    Blog author for snippets.
    """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                ImageChooserPanel('image'),
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
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogPageGalleryInfo(Orderable):
    """
    Holds the title and description for an in-page image gallery.
    """
    gallery_info = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_info')
    gallery_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Title')
    gallery_description = models.CharField(max_length=250, null=True, blank=True, verbose_name='Description')
