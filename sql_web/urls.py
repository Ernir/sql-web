from django.conf.urls import url
from sql_web import views

urlpatterns = [
    url(r"^vidfangsefni/$", views.sections, name="sections"),
    url(r"^vidfangsefni/(?P<section_slug>.+)/$", views.section,
        name="section"),
]