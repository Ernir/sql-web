from django.core.exceptions import ObjectDoesNotExist
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
from sql_web.models import Figure
import base64, hashlib

class FigureExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {}
        super(FigureExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        FIGURE_RE = r'\!\[(?P<alt>.*)\]\( *?(?P<url>[^ ]+) *?(?:"(?P<text>.*?)")?\)'
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
        if m.group("text"):
            text = m.group("text")
        else:
            text = alt
        try:
            # This whole exercise is to make it possible to reference figures by identifier.
            # If the argument is not a valid figure identifier, fall back to using it as an url.
            figure = Figure.objects.get(identifier=main_argument)
            url = figure.get_absolute_url()
        except ObjectDoesNotExist:
            url = main_argument

        # Generating a likely-to-be-unique identifier
        identifier = hashlib.sha224(base64.urlsafe_b64decode(url)).hexdigest()
        

        figure_element = etree.Element("figure")
        label = etree.SubElement(figure_element, "label")
        label.set("for", "figure-{}".format(identifier))
        label.set("class", "margin-toggle")
        label.text = "⊕"
        input_element = etree.SubElement(figure_element, "input")
        input_element.set("type", "checkbox")
        input_element.set("id", "figure-{}".format(identifier))
        input_element.set("class", "margin-toggle")
        text_span = etree.SubElement(figure_element, "span")
        text_span.set("class", "marginnote")
        text_span.text = text
        image = etree.SubElement(figure_element, "img")
        image.set("src", url)
        image.set("alt", alt)
        return figure_element


def makeExtension(*args, **kwargs):
    return FigureExtension(*args, **kwargs)
