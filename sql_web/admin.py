from django.contrib import admin
from sql_web.forms import AceEditorAdminModelForm
from sql_web.models import Section, Example, Exercise, Subject, Figure

admin.site.register(Subject)
admin.site.register(Example)
admin.site.register(Exercise)


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    form = AceEditorAdminModelForm
