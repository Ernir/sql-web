from django.template import Template, Context
from django import template
from django.template.defaultfilters import stringfilter
from sql_web.models import Section

register = template.Library()


@register.inclusion_tag("snippets/footnote.html", takes_context=True)
def footnote(context, text_contents):
    """
    A template tag to turn {{ footnote "text contents" }} into a
    tufte_css sidenote.
    """

    # Each sidenote needs its own ID.
    if "footnote_count" not in context:
        context["footnote_count"] = 0
    else:
        context["footnote_count"] += 1

    footnote_id = str(context["footnote_count"])
    return {
        "footnote_text": text_contents,
        "footnote_id": footnote_id
    }

@register.inclusion_tag("snippets/reference.html")
def ref(reference_id):
    section = Section.objects.get(identifier=reference_id)
    return {
        "sec": section
    }


@register.filter
@stringfilter
def render(value):
    """
    A template filter that renders the given string as a Django template.
    """
    return Template("{% load sql_shortcuts %}" + value).render(Context())