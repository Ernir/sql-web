from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from sql_web.forms import ExerciseForm
from sql_web.models import Section, Exercise


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
    Defines pages and returns data related to individual lexical sections.
    """

    def get(self, request, section_slug):
        """
        Finds and displays a section based on its slugified title,
        passed in by section_slug.
        """
        the_section = get_object_or_404(Section, slug=section_slug)
        self.params["section"] = the_section
        self.params["title"] = the_section.title
        return render(request, "section.html", self.params)


class SectionListView(BaseView):
    """
    A list of all sections.
    """

    def get(self, request):
        the_sections = Section.objects.all()
        self.params["sections"] = the_sections
        self.params["title"] = "Yfirlitssíða"
        return render(request, "sections.html", self.params)


class ExerciseView(BaseView):
    """
    Defines the page of an individual exercise.
    """

    def get(self, request, exercise_slug):
        the_exercise = get_object_or_404(
            Exercise,
            identifier=exercise_slug
        )
        data = {"code_area": the_exercise.prepopulated}
        form = ExerciseForm(initial=data)

        self.params["form"] = form
        self.params["exercise"] = the_exercise

        return render(request, "exercise.html", self.params)


def index(request):
    pass  # ToDo make one