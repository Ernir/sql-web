from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View
from sql_web.forms import ExerciseForm
from sql_web.models import Section, Exercise, Subject
from sql_web.sql_runner import ExerciseRunner


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

        if not request.user.is_anonymous():
            the_section.read_by.add(request.user)

        self.params["section"] = the_section
        self.params["title"] = the_section.title
        return render(request, "section.html", self.params)


class SectionListView(BaseView):
    """
    A list of all sections.
    """

    def get(self, request):
        subjects = Subject.objects.all()
        self.params["subjects"] = subjects
        self.params["title"] = "Yfirlitssíða"
        return render(request, "sections.html", self.params)


class ProfileView(BaseView):
    """
    A single user's profile
    """

    @method_decorator(login_required)
    def get(self, request):
        read_sections = request.user.read.all()

        unread_sections = []
        num_unread_to_show = 5
        # Find some unread sections connected to those previously read
        for section in read_sections:
            connected_sections = [
                s for s in section.connected_to.all()
                if request.user not in s.read_by.all()
                ]
            for conn in connected_sections:
                if request.user not in conn.read_by.all() \
                        and conn not in unread_sections:
                    unread_sections.append(conn)
            if len(unread_sections) >= num_unread_to_show:
                unread_sections = unread_sections[:num_unread_to_show]
                break

        self.params["read_sections"] = read_sections
        self.params["unread_sections"] = unread_sections

        return render(request, "profile.html", self.params)


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

    def post(self, request, exercise_slug):

        form = ExerciseForm(request.POST)

        if form.is_valid():
            the_exercise = get_object_or_404(
                Exercise,
                identifier=exercise_slug
            )

            self.params["form"] = form
            self.params["exercise"] = the_exercise

            schema = the_exercise.given_schema
            to_emulate = the_exercise.sql_to_emulate
            statements = form.cleaned_data["code_area"]
            statement_type = "DDL"

            runner = ExerciseRunner(
                statements, schema, to_emulate, statement_type
            )

            valid = runner.is_valid()
            print(valid)

            return render(request, "exercise.html", self.params)
        else:
            return self.get(request, exercise_slug)


def index(request):
    pass  # ToDo make one


"""
Non-user visible views - JSON endpoints and similar
"""


class SectionOverview(View):
    def get(self, request):
        sections = Section.objects.all()
        data = {
            "nodes": [],
            "links": []
        }
        for section in sections:
            read = section.read_by.filter(id=request.user.id).exists()
            data["nodes"].append({
                "name": section.title,
                "group": section.subject.id,
                "id": section.id,
                "location": section.get_absolute_url(),
                "read": read,
            })
            for connection in section.connected_to.all():
                data["links"].append({
                    "source": section.id, "target": connection.id,
                    "value": 1
                })
        return JsonResponse(data)


def handler404(request):
    response = render_to_response('404.html', {"title": "Síða fannst ekki!"}, context_instance=RequestContext(request))
    response.status_code = 404
    return response
