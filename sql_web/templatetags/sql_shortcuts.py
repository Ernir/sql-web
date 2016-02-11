from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django import template
from django.template.defaultfilters import stringfilter
from sql_web.models import Section, Figure

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
    try:
        section = Section.objects.get(identifier=reference_id)
    except ObjectDoesNotExist:
        section = None  # Handle missing references in the templates

    return {"sec": section}


@register.inclusion_tag("snippets/figure.html")
def figure(reference_id):
    try:
        fig = Figure.objects.get(identifier=reference_id)
    except ObjectDoesNotExist:
        fig = None  # Handle missing references in the templates
    return {
        "figure": fig
    }


@register.filter
@stringfilter
def render(value):
    """
    A template filter that renders the given string as a Django template.
    """
    return Template("{% load sql_shortcuts %}" + value).render(Context())