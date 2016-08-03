from django.contrib import admin
from sql_web.models import Section, Example, Exercise, Subject, Figure, Assignment, Footnote, IndexText, Course
from adminsortable2.admin import SortableAdminMixin

admin.site.register(Subject)
admin.site.register(Example)
admin.site.register(Exercise)
admin.site.register(Footnote)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ["assignments", "members"]
    exclude = ("rendered_description", "slug")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    filter_horizontal = ["connected_to"]
    exclude = ("read_by", "rendered_contents")
    readonly_fields = ("slug",)


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    filter_horizontal = ["exercises", "reading", "assigned_to"]


@admin.register(IndexText)
class IndexTextAdmin(SortableAdminMixin, admin.ModelAdmin):
    exclude = ("rendered_contents",)
