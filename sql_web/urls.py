from django.conf.urls import patterns, url
from sql_web import views

urlpatterns = \
    patterns(
        '',

        url(r"^vidfangsefni/$", views.sections, name="sections"),
        url(r"^vidfangsefni/(?P<section_slug>.+)/$", views.section, name="section"),
    )