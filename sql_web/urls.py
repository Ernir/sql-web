from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from sql_web import views
from sql_web.forms import UserCreationForm

urlpatterns = [
    # User-facing
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^vidfangsefni/$", views.SectionListView.as_view(), name="sections"),
    url(r"^vidfangsefni/(?P<section_slug>.+)/$", views.SectionView.as_view(), name="section"),
    url(r"^aefingar/$", views.ExerciseListView.as_view(), name="exercises"),
    url(r"^aefing/(?P<exercise_slug>.+)/$", views.ExerciseView.as_view(), name="exercise"),
    url(r"^min-sida/$", views.ProfileView.as_view(), name="profile"),
    url(r"^skraning/$",
        CreateView.as_view(template_name='registration/register.html', form_class=UserCreationForm, success_url='/'),
    name = "custom_register"),
    url(r"^utskraning/$", views.LogoutView.as_view(), name="custom_logout", ),
    url(r"^namskeid/(?P<course_slug>.+)/$", views.CourseView.as_view(), name="course"),

    # Not for the users:
    url(r"^bakatil/vidfangsefni/$", views.SectionOverview.as_view(),
        name="section_overview"),
    url(r"^bakatil/vidfangsefni/(?P<subject_id>\d+)/$", views.SectionOverview.as_view(),
        name="single_section_overview"),
    url('^accounts/', include('django.contrib.auth.urls')),
]
