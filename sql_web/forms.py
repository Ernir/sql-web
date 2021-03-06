from django import forms
from django_ace import AceWidget
from sql_web.models import Section
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(forms.ModelForm):
    """
    Customized version of the form in auth/forms.py.
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Sláðu inn sama lykilorð og að ofan, til staðfestingar."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AceEditorAdminModelForm(forms.ModelForm):
    html_contents = forms.CharField(
        widget=AceWidget(
            mode='html',
            width="600px",
            height="1000px",
            wordwrap=True
        ),
    )

    class Meta:
        exclude = ("slug",)
        model = Section


class ExerciseForm(forms.Form):
    code_area = forms.CharField(label="Sláðu inn SQL-skipun:", widget=forms.Textarea)


class CourseRegistrationForm(forms.Form):
    directive = forms.BooleanField(label="Hakaðu hér og ýttu á takkann til að skrá þig í námskeiðið.")


class SettingsChangeForm(forms.Form):
    CHOICES = [
        (False, "Slökkt á Javascript"),
        (True, "Kveikt á Javascript")
    ]
    js_enabled = forms.ChoiceField(label="Nota JavaScript á yfirlitssíðu (myndir)", choices=CHOICES, widget=forms.RadioSelect)
