from django.shortcuts import get_object_or_404, render
from sql_web.models import Section


def section(request, section_slug):
    """
    Defines the page of a single lexical section.
    Finds the section based on its slugified title,
    passed in by section_slug.
    """

    the_section = get_object_or_404(Section, slug=section_slug)
    return render(request, "section.html", {"section": the_section})


def sections(request):
    """
    A list of all sections.
    """

    the_sections = Section.objects.all()
    return render(request, "sections.html", {"sections": the_sections})


def index(request):
    pass # ToDo make one