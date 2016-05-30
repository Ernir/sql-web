import hashlib

from django.core.exceptions import ObjectDoesNotExist
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
from sql_web.models import Figure, Example


class FigureExtension(Extension):
    """
    A Markdown extension for tufte-css style figures.

    Figures use the following format:

    ![alt text][figure_identifier "Descriptive text for the figure"]

    Which is similar to the Markdown image inclusion strategy in the specification. However, here figure_identifier is
    assumed to be the identifier of a sql_web.models.Figure instance. It is parsed as an URL only if no matching Figure
    is found.
    The figure identifier may not contain spaces.

    Two additional qualifiers can be prefixed to the pattern:

    * "f" makes the figure a fullwidth tufte-figure
    * "m" makes the figure a Tufte marginfigure

    So

    f![alt text](figure_identifier "Descriptive text for the full-width figure")

    is a full-width figure.
    """

    def __init__(self, *args, **kwargs):
        self.config = {}
        super(FigureExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        FIGURE_RE = r'(?P<qualifier>f|m?)\!\[(?P<alt>.*)\]\( *?(?P<url>[^ ]+) *?(?:"(?P<text>.*?)")?\)'
        figure_pattern = Figures(FIGURE_RE, self.getConfigs())
        figure_pattern.md = md
        md.inlinePatterns.add('new_image_link', figure_pattern, "<image_link")


class Figures(Pattern):
    def __init__(self, pattern, config):
        super(Figures, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        alt = m.group("alt")
        main_argument = m.group("url")
        print(main_argument)
        if m.group("text"):
            text = m.group("text")
        else:
            text = alt

        full_width, marginfigure = False, False
        if m.group("qualifier"):
            full_width = m.group("qualifier") == "f"
            marginfigure = m.group("qualifier") == "m"

        figure = None
        try:
            figure = Figure.objects.get(identifier=main_argument)
        except ObjectDoesNotExist:
            pass  # This is not exceptional

        example = None
        if not figure:
            try:
                example = Example.objects.get(identifier=main_argument)
                text = example.description
            except ObjectDoesNotExist:
                pass

        url = ""
        if figure:
            url = figure.image.url
            to_encode = url
        elif example:
            code = example.code
            to_encode = code
        else:
            url = main_argument
            to_encode = url

        # Generating a likely-to-be-unique identifier
        identifier = hashlib.sha224(str.encode(to_encode)).hexdigest()

        # ToDo simplify this monster
        if not marginfigure:
            root = etree.Element("figure")
            if full_width:
                root.set("class", "fullwidth")
            label = etree.SubElement(root, "label")
            label.set("for", "figure-{}".format(identifier))
            label.set("class", "margin-toggle")
            label.text = "⊕"
            input_element = etree.SubElement(root, "input")
            input_element.set("type", "checkbox")
            input_element.set("id", "figure-{}".format(identifier))
            input_element.set("class", "margin-toggle")
            if not full_width:
                text_span = etree.SubElement(root, "span")
                text_span.set("class", "marginnote")
                text_span.text = text
            if figure:
                image_element = etree.SubElement(root, "img")
                image_element.set("src", figure.image.url)
                image_element.set("alt", alt)
            elif example:
                code_element = etree.SubElement(root, "pre")
                code_element.set("class", "code prettyprint {}".format(example.language))
                code_element.text = example.code
        else:
            root = etree.Element("span")
            label = etree.SubElement(root, "label")
            label.set("for", "figure-{}".format(identifier))
            label.set("class", "margin-toggle")
            label.text = "⊕"
            input_element = etree.SubElement(root, "input")
            input_element.set("type", "checkbox")
            input_element.set("id", "figure-{}".format(identifier))
            input_element.set("class", "margin-toggle")
            margin_wrapper = etree.SubElement(root, "span")
            margin_wrapper.set("class", "marginnote")
            image_element = etree.SubElement(margin_wrapper, "img")
            image_element.set("src", url)
            image_element.set("alt", alt)
            etree.SubElement(margin_wrapper, "br")  # Force line break
            text_span = etree.SubElement(margin_wrapper, "span")
            text_span.text = text
        return root


def makeExtension(*args, **kwargs):
    return FigureExtension(*args, **kwargs)
