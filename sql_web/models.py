from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.template import Template, Context

"""
Models to display and organize text
"""


class Subject(models.Model):
    """
    A common topic shared by one or more sections.
    """

    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Section(models.Model):
    """
    A body of explanatory text appearing on a single page.
    """

    identifier = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject)
    html_contents = models.TextField()
    rendered_contents = models.TextField()
    connected_to = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False
    )
    read_by = models.ManyToManyField(User, blank=True, related_name="read")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("section", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        context = Context({"section": self})

        for footnote in self.footnote_set.all():
            footnote.delete()

        self.rendered_contents = Template(
            "{% load sql_shortcuts %}" + self.html_contents
        ).render(context)

        super(Section, self).save(*args, **kwargs)


"""
Models to store information about assignments
"""


class Exercise(models.Model):
    """
    A description of a problem to solve, along with a definition of the
    "correct" result.
    """

    identifier = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    problem_description = models.TextField()
    prepopulated = models.TextField()
    given_schema = models.TextField(blank=True)
    sql_to_emulate = models.TextField()

    def get_absolute_url(self):
        return reverse("exercise", args=[self.identifier])

    def __str__(self):
        return self.identifier


class Assignment(models.Model):
    """
    A group of exercises to complete and sections to read
    """

    exercises = models.ManyToManyField(Exercise, blank=True)
    reading = models.ManyToManyField(Section, blank=True)

    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    assigned_to = models.ManyToManyField(User, blank=True)


"""
Other models
"""


class Example(models.Model):
    """
    A code listing, contained within a section.
    """

    identifier = models.CharField(max_length=50, unique=True)
    code = models.TextField()
    description = models.TextField()

    sql, php = "lang-sql", "lang-php"
    LANGUAGE_CHOICES = (
        (sql, "SQL"),
        (php, "PHP")
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default=sql
    )

    def __str__(self):
        return "{0}: {1}".format(self.language, self.identifier)


class Figure(models.Model):
    """
    An image to be displayed as a part of a text body.
    """

    identifier = models.CharField(max_length=50, unique=True)
    short_description = models.CharField(max_length=200, blank=True)
    full_description = models.TextField()
    image = models.ImageField()

    def image_tag(self):
        return '<img src="{0}" style="max-width: 100%"/>'.format(
            self.image.url
        )

    image_tag.short_description = "Forskoðun"
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if not (self.short_description):
            self.short_description = self.full_description[:200]
        super(Figure, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.short_description, self.identifier)


class Footnote(models.Model):
    """
    Additional comments, related to a section's body of text
    """
    identifier = models.CharField(max_length=50)
    section = models.ForeignKey(Section)
    raw_contents = models.TextField()
    rendered_contents = models.TextField()

    def get_absolute_url(self):
        return self.section.get_absolute_url() + "#footnote-" + self.identifier

    def __str__(self):
        return self.identifier

    def save(self, *args, **kwargs):
        context = Context({"section": self})
        self.rendered_contents = Template(
            "{% load sql_shortcuts %}" + self.raw_contents
        ).render(context)

        super(Footnote, self).save(*args, **kwargs)