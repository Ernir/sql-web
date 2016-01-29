from django.contrib import admin
from sql_web.forms import AceEditorAdminModelForm
from sql_web.models import Section, Example, Exercise, Subject

admin.site.register(Subject)
admin.site.register(Example)
admin.site.register(Exercise)


class SectionAdmin(admin.ModelAdmin):
    form = AceEditorAdminModelForm

admin.site.register(Section, SectionAdmin)