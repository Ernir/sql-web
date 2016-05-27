from markdown.util import etree
from markdown import Extension
from markdown.inlinepatterns import Pattern
from sql_web.models import Footnote, Section


class FootnoteExtension(Extension):
    """
    A Markdown extension for tufte-css style footnotes.

    Footnotes use the following format:

    [^identifier][contents]

    Where identifier is a (preferably unique) identifier for the footnote in question, and contents are the text the
    footnote contains. The identifier must be prefixed with a ^, which is not a part of the identifier.

    When the resulting structure is processed by tufte-css, it is displayed as a "side-footnote"
    """
    def __init__(self, *args, **kwargs):
        self.config = {"section": ["", "The identifier of a single lexical section"]}
        super(FootnoteExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        FOOTNOTE_RE = r'\[\^(?P<identifier>[a-z\d#-_]+)\]\[(?P<text>.*)\]'
        footnote_pattern = Footnotes(FOOTNOTE_RE, self.getConfigs())
        footnote_pattern.md = md
        md.inlinePatterns.add('footnote', footnote_pattern, "<not_strong")


class Footnotes(Pattern):
    def __init__(self, pattern, config):
        self.config = config
        super(Footnotes, self).__init__(pattern)


    def handleMatch(self, m):
        identifier = m.group("identifier")
        text = m.group("text")

        section = Section.objects.get(identifier=self.config["section"])
        fn = Footnote.objects.create(identifier=identifier, contents=text, section=section)
        fn.save()

        span = etree.Element("span")
        label = etree.SubElement(span, "label")
        label.set("for", "footnote-{}".format(identifier))
        label.set("class", "margin-toggle sidenote-number")
        input_element = etree.SubElement(span, "input")
        input_element.set("type", "checkbox")
        input_element.set("id", "footnote-{}".format(identifier))
        input_element.set("class", "margin-toggle")
        text_span = etree.SubElement(span, "span")
        text_span.set("class", "sidenote")
        text_span.text = text

        return span


def makeExtension(*args, **kwargs):
    """Return extension."""

    return FootnoteExtension(*args, **kwargs)
