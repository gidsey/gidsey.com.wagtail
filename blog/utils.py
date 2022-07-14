from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(request, queryset, num_items):
    """"
    Paginate results.
    """
    paginator = Paginator(queryset, num_items)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def get_tags(request, context, all_posts):
    if request.GET.get('tag', None):
        tag = request.GET.get('tag')
        context['selected_tag'] = tag
        all_posts = all_posts.filter(tags__slug__in=[tag])
    return context, all_posts
