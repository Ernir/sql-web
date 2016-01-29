from django import forms
from django_ace import AceWidget
from sql_web.models import Section


class AceEditorAdminModelForm(forms.ModelForm):
    html_contents = forms.CharField(
        widget=AceWidget(
            mode='html',
            width="1000px",
            wordwrap=True
        ),
    )

    class Meta:
        exclude = ("slug", )
        model = Section