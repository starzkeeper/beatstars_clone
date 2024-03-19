from django import template
from django.template.defaultfilters import urlencode

register = template.Library()


@register.inclusion_tag('search/search_field.html', takes_context=True)
def search_field(context, value, **kwargs):
    context.update({'query_value': value})
    return context


@register.simple_tag(takes_context=True)
def append_query_to_url(context, url):
    return '{}?search={}'.format(url, urlencode(context.get('search', '')))


@register.inclusion_tag('search/found_objects.html', takes_context=True)
def found_objects(context, results, results_count, objects_title, all_search_message, search_url):
    context.update({
        'results': results,
        'results_count': results_count,
        'objects_title': objects_title,
        'all_search_message': all_search_message,
        'search_url': search_url
    })
    return context
