from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from sql_web.models import Section


class BaseView(View):
    """
    An "abstract view" to manage the elements all of the site's
    pages have in common
    """

    def __init__(self):
        super().__init__()
        self.params = {
            "title": "SQL kennslusíða",  # Default value
        }


class SectionView(BaseView):
    """
    Defines the page of a single lexical section.
    Finds the section based on its slugified title,
    passed in by section_slug.
    """

    def get(self, request, section_slug):
        the_section = get_object_or_404(Section, slug=section_slug)
        self.params["section"] = the_section
        self.params["title"] = the_section.title
        return render(request, "section.html", self.params)


def sections(request):
    """
    A list of all sections.
    """

    the_sections = Section.objects.all()
    return render(request, "sections.html", {"sections": the_sections})


def index(request):
    pass  # ToDo make one