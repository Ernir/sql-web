from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from markdown import markdown
from sql_web.markdown_extensions.inline_code import InlineCodeExtension
from sql_web.text_processing import apply_markdown

"""
Models to display and organize text
"""


class Subject(models.Model):
    """
    A common topic shared by one or more sections.
    """

    title = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("number",)


class Section(models.Model):
    """
    A body of explanatory text appearing on a single page.
    """

    identifier = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    subject = models.ForeignKey(Subject)
    contents = models.TextField()
    rendered_contents = models.TextField()
    connected_to = models.ManyToManyField('self', blank=True, symmetrical=False)
    associated_exercises = models.ManyToManyField("Exercise", blank=True)
    read_by = models.ManyToManyField(User, blank=True, related_name="read")

    def __str__(self):
        return "K{}: {}".format(self.subject.number, self.title)

    def get_absolute_url(self):
        return reverse("section", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Section, self).save(*args, **kwargs)

        for footnote in self.footnote_set.all():
            footnote.delete()  # These will be re-generated by the Markdown processor

        self.rendered_contents = apply_markdown(self.contents, self.identifier)

        super(Section, self).save(*args, **kwargs)

    class Meta:
        ordering = ("subject__number", "title")


class Example(models.Model):
    """
    A code listing, contained within a section.
    """

    identifier = models.CharField(max_length=50, unique=True)
    code = models.TextField()
    description = models.TextField()

    sql, php, python, java, bash = "lang-sql", "lang-php", "lang-python", "lang-java", "lang-bash"
    LANGUAGE_CHOICES = (
        (sql, "SQL"),
        (php, "PHP"),
        (python, "Python"),
        (java, "Java"),
        (bash, "Bash")
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
    description = models.TextField()
    image = models.ImageField()

    def image_tag(self):
        return '<img src="{0}" style="max-width: 100%"/>'.format(
            self.image.url
        )

    image_tag.short_description = "Forskoðun"
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if self.identifier[:5] != "mynd:":
            self.identifier = "mynd:" + self.identifier
        super(Figure, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.description[:50], self.identifier)


class Footnote(models.Model):
    """
    Additional comments, related to a section's body of text
    """
    identifier = models.CharField(max_length=50)
    contents = models.TextField()
    section = models.ForeignKey(Section)

    def get_absolute_url(self):
        return "#footnote-" + self.identifier

    def __str__(self):
        return "{} ({})".format(self.section.title, self.identifier)


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
    rendered_description = models.TextField()
    prepopulated = models.TextField(blank=True)
    given_schema = models.TextField(blank=True)
    sql_to_emulate = models.TextField()

    DDL = "DDL"
    DML = "DML"
    STATEMENT_TYPE_CHOICES = ((DDL, "Other"), (DML, "SELECT"))
    statement_type = models.CharField(max_length=3, choices=STATEMENT_TYPE_CHOICES, default=DML)

    completed_by = models.ManyToManyField(User, blank=True)

    def get_absolute_url(self):
        return reverse("exercise", args=[self.identifier])

    def __str__(self):
        return self.identifier

    def save(self, *args, **kwargs):
        self.rendered_description = markdown(self.problem_description, extensions=["tables", InlineCodeExtension()])
        super(Exercise, self).save(*args, **kwargs)


class Assignment(models.Model):
    """
    A group of exercises to complete and sections to read
    """

    exercises = models.ManyToManyField(Exercise, blank=True)
    reading = models.ManyToManyField(Section, blank=True)

    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    assigned_to = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "Verkefni, í gildi frá {} til {}".format(str(self.time_start), str(self.time_end))


class Course(models.Model):
    """
    Students are organized into courses
    """

    name = models.CharField(max_length=200, unique=True)
    open_to_all = models.BooleanField(default=True, help_text="Sé áfanginn lokaður sérð þú um að skrá inn nemendur")
    assignments = models.ManyToManyField(Assignment, blank=True)
    members = models.ManyToManyField(User, blank=True)
    description = models.TextField()

    rendered_description = models.TextField()
    slug = models.SlugField(max_length=200)

    def get_absolute_url(self):
        return reverse("course", args=[self.slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ToDo handle assignments
        self.slug = slugify(self.name)
        self.rendered_description = markdown(self.description, extensions=["tables", InlineCodeExtension()])
        super(Course, self).save(*args, **kwargs)


"""
Other models
"""


class IndexText(models.Model):
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    contents = models.TextField()
    rendered_contents = models.TextField()

    def save(self, *args, **kwargs):
        self.rendered_contents = markdown(self.contents, extensions=["tables", InlineCodeExtension()])
        super(IndexText, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ('order',)
