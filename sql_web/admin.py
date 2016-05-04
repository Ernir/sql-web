from django.contrib import admin
from sql_web.forms import AceEditorAdminModelForm
from sql_web.models import Section, Example, Exercise, Subject, Figure, \
    Assignment

admin.site.register(Subject)
admin.site.register(Example)
admin.site.register(Exercise)


@admin.register(Section)
class SubjectAdmin(admin.ModelAdmin):
    form = AceEditorAdminModelForm
    filter_horizontal = ["connected_to"]
    exclude = ["read_by"]
    readonly_fields = ("rendered_contents", )


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    filter_horizontal = ["exercises", "reading", "assigned_to"]