from django.contrib import admin
from sql_web.models import Section, Example, Exercise, Subject, Figure, Assignment, Footnote

admin.site.register(Subject)
admin.site.register(Example)
admin.site.register(Exercise)
admin.site.register(Footnote)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    filter_horizontal = ["connected_to"]
    exclude = ("read_by", "html_contents")
    readonly_fields = ("slug", "rendered_contents")


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    filter_horizontal = ["exercises", "reading", "assigned_to"]
