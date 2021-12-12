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
