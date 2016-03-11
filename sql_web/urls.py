from django.conf.urls import url
from sql_web import views

urlpatterns = [
    # User-facing
    url(r"^vidfangsefni/$", views.SectionListView.as_view(), name="sections"),
    url(r"^vidfangsefni/(?P<section_slug>.+)/$",
        views.SectionView.as_view(), name="section"),
    url(r"^verkefni/(?P<exercise_slug>.+)/$", views.ExerciseView.as_view(),
        name="exercise"),
    url(r"^profile/$", views.ProfileView.as_view(), name="profile"),

    # Not for the users:
    url(r"^bakatil/vidfangsefni/$", views.SectionOverview.as_view(), name="section_overview")
]