from django.contrib import admin
from sql_web.models import Section, Example, Exercise, Subject, Figure, Assignment, Footnote, IndexText, Course
from adminsortable2.admin import SortableAdminMixin

admin.site.register(Subject)
admin.site.register(Example)
admin.site.register(Footnote)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    filter_horizontal = ["completed_by", ]
    exclude = ("rendered_description",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ["members"]
    exclude = ("rendered_description", "slug")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    filter_horizontal = ["connected_to", "associated_exercises"]
    exclude = ("read_by", "rendered_contents")
    readonly_fields = ("slug", "distance")


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    filter_horizontal = ["exercises", "reading", "assigned_students"]


@admin.register(IndexText)
class IndexTextAdmin(SortableAdminMixin, admin.ModelAdmin):
    exclude = ("rendered_contents",)
