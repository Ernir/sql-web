from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django import template
from django.template.defaultfilters import stringfilter
from sql_web.models import Section, Figure, Example

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


def find_figure(reference_id):
    try:
        fig = Figure.objects.get(identifier=reference_id)
    except ObjectDoesNotExist:
        fig = None  # Handle missing references in the templates
    return {
        "figure": fig
    }


@register.inclusion_tag("snippets/figure.html")
def figure(reference_id):
    return find_figure(reference_id)


@register.inclusion_tag("snippets/marginfigure.html", takes_context=True)
def marginfigure(context, reference_id):
    # Each margin figure needs its own ID.
    if "marginfigure_count" not in context:
        context["marginfigure_count"] = 0
    else:
        context["marginfigure_count"] += 1
    marginfigure_id = str(context["marginfigure_count"])

    figure_reference = find_figure(reference_id)
    figure_reference.update({"marginfigure_id": marginfigure_id})

    return figure_reference


def find_example(reference_id):
    try:
        example = Example.objects.get(identifier=reference_id)
    except ObjectDoesNotExist:
        example = None  # Handle missing references in the templates
    return {"example": example}


@register.inclusion_tag("snippets/examplecode.html")
def code(reference_id):
    return find_example(reference_id)


@register.filter
@stringfilter
def render(value):
    """
    A template filter that renders the given string as a Django template.
    """
    return Template("{% load sql_shortcuts %}" + value).render(Context())