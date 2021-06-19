from django import template

register = template.Library()

@register.filter(name="tag_value")
def tag_value(value):
    return value.getlist("tags")

@register.filter(name="get_link")
def get_link(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist("tags"):
        tags = new_request.getlist("tags")
        tags.remove(tag.slug)
        new_request.setlist("tags", tags)
    else:
        new_request.appendlist("tags", tag.slug)

    return new_request.urlencode()
