from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View
from sql_web.forms import ExerciseForm, CourseRegistrationForm, SettingsChangeForm
from sql_web.models import Section, Exercise, Subject, IndexText, Course
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


class IndexView(BaseView):
    def get(self, request):
        self.params["title"] = "Upphafssíða"
        self.params["index_page_content"] = IndexText.objects.all()
        return render(request, "index.html", self.params)


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

        if not the_section.visible and not request.user.is_superuser:
            return render(request, "hidden.html", self.params)

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

        for s in subjects:
            if s.best_start and request.user in s.best_start.read_by.all():
                s.best_start.necessary = False

        self.params["subjects"] = subjects
        self.params["title"] = "Yfirlitssíða viðfangsefna"
        self.params["js_enabled"] = request.user.is_anonymous() or request.user.userprofile.js_enabled
        return render(request, "sections.html", self.params)


class ProfileView(BaseView):
    """
    A single user's profile
    """

    @method_decorator(login_required)
    def get(self, request):
        form = SettingsChangeForm(initial={"js_enabled": request.user.userprofile.js_enabled})
        self.params["form"] = form
        return self.profile_view_common(request)

    @method_decorator(login_required)
    def post(self, request):
        form = SettingsChangeForm(request.POST)
        if form.is_valid():
            profile = request.user.userprofile
            profile.js_enabled = form.cleaned_data["js_enabled"] == "True"
            profile.save()
        else:  # Change nothing
            pass
        self.params["form"] = form
        return self.profile_view_common(request)

    def profile_view_common(self, request):
        currently_member_of = request.user.course_set.all()
        available_courses = Course.objects.filter(open_to_all=True).all()
        # Manual filtering due to ORM limitations. ToDO find prettier way.
        available_courses = [course for course in available_courses if course not in currently_member_of]

        read_sections = request.user.read.all()
        unread_sections = []
        num_unread_to_show = 5
        # Find some unread sections connected to those previously read
        for read_section in read_sections:
            connected_sections = [
                rs for rs in read_section.connected_to.filter(visible=True).all()
                if request.user not in rs.read_by.all()
                ]
            for conn in connected_sections:
                if request.user not in conn.read_by.all() \
                        and conn not in unread_sections:
                    unread_sections.append(conn)
            if len(unread_sections) >= num_unread_to_show:
                unread_sections = unread_sections[:num_unread_to_show]
                break

        self.params["available_courses"] = available_courses
        self.params["currently_member_of"] = currently_member_of
        self.params["read_sections"] = read_sections
        self.params["unread_sections"] = unread_sections
        self.params["title"] = "Síðan mín"

        return render(request, "profile.html", self.params)


class LogoutView(BaseView):
    def get(self, request):
        logout(request)
        return redirect("index")


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
        with ExerciseRunner(the_exercise.prepopulated, the_exercise) as runner:
            if the_exercise.given_schema:
                self.params["schema_display"] = runner.parse_schema()
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

            user_statements = form.cleaned_data["code_area"]

            with ExerciseRunner(user_statements, the_exercise) as runner:
                valid, message = runner.is_valid()
                self.params["message"] = message

                if valid and request.user.is_authenticated():
                    the_exercise.completed_by.add(request.user)

                if the_exercise.given_schema:
                    self.params["schema_display"] = runner.parse_schema()
            return render(request, "exercise.html", self.params)
        else:
            return self.get(request, exercise_slug)


class ExerciseListView(BaseView):
    """
    A list of all defined exercises.
    """

    def get(self, request):
        exercises = Exercise.objects.all()
        completed_exercises, not_completed_exercises = [], []
        for e in exercises:
            if request.user in e.completed_by.all():
                completed_exercises.append(e)
            else:
                not_completed_exercises.append(e)
        self.params["complete"] = completed_exercises
        self.params["incomplete"] = not_completed_exercises
        self.params["title"] = "Yfirlitssíða verkefna"
        return render(request, "exercises.html", self.params)


class CourseView(BaseView):
    def get(self, request, course_slug):
        the_course = get_object_or_404(Course, slug=course_slug)
        return self.course_view_common(request, the_course)

    def post(self, request, course_slug):
        the_course = get_object_or_404(Course, slug=course_slug)
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            if "directive" in request.POST and request.POST["directive"] == "on":
                the_course.members.add(request.user)
        return self.course_view_common(request, the_course)

    def course_view_common(self, request, the_course):
        self.params["course"] = the_course
        self.params["registered"] = request.user in the_course.members.all()
        self.params["form"] = CourseRegistrationForm()
        return render(request, "course.html", self.params)


"""
Non-user visible views - JSON endpoints and similar
"""


class SectionOverview(View):
    """
    Used to return the context data for the sections.
    It is returned in JSON format, as an object containing node and link references.
    """

    def get(self, request, subject_id=None):
        data = {
            "nodes": [],
            "links": [],
        }
        sections_query = Section.objects.filter(visible=True)
        if subject_id:  # It is possible to specifify a specific subject
            subject = get_object_or_404(Subject, id=subject_id)
            sections_query = sections_query.filter(subject=subject)
            data["subject"] = int(subject_id)
        sections = sections_query.all()

        # Generate the vertices:
        data["nodes"] = {}
        for section in sections:
            data["nodes"][section.id] = {
                "name": section.title,
                "location": section.get_absolute_url(),
            }

        # Generate the edges
        for section in sections:
            for connection in section.connected_to.all():
                if connection.visible and connection.subject == section.subject:
                    data["links"].append({"source": section.id, "target": connection.id})
        return JsonResponse(data)


def handler404(request):
    response = render_to_response('404.html', {"title": "Síða fannst ekki!"}, context_instance=RequestContext(request))
    response.status_code = 404
    return response
