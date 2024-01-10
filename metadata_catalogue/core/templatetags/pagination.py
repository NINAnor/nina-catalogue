from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()


@register.simple_tag
def page_result(page_object, **kwargs):
    first = ((page_object.number - 1) * page_object.paginator.per_page) + 1
    first = first if page_object.paginator.count > 0 else 0
    second = (page_object.number * page_object.paginator.per_page) + 1
    second = second if second < page_object.paginator.count else page_object.paginator.count
    return f"{first}-{second} of {page_object.paginator.count} results"
