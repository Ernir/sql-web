from markdown.util import etree
from markdown import Extension
from markdown.inlinepatterns import Pattern

RE_SMART_CONTENT = r'((?:[^\=]|\=(?=[^\W_]|\=|\s)|(?<=\s)\=+?(?=\s))+?\=*?)'
RE_DUMB_CONTENT = r'((?:[^\=]|(?<!\=)\=(?=[^\W_]|\=))+?)'
RE_SMART_MARK_BASE = r'(\={2})(?![\s\=])%s(?<!\s)\={2}' % RE_SMART_CONTENT
RE_SMART_MARK = r'(?:(?<=_)|(?<![\w\=]))%s(?:(?=_)|(?![\w\=]))' % RE_SMART_MARK_BASE
RE_MARK_BASE = r'(\={2})(?!\s)%s(?<!\s)\={2}' % RE_DUMB_CONTENT
RE_MARK = RE_MARK_BASE


class FootnoteExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.config = {}
        super(FootnoteExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs()

        # append to end of inline patterns
        FOOTNOTE_RE = r'\[\^(?P<identifier>[a-z\d#-_]+)\]\[(?P<text>.*)\]'
        footnote_pattern = Footnotes(FOOTNOTE_RE, self.getConfigs())
        footnote_pattern.md = md
        md.inlinePatterns.add('footnote', footnote_pattern, "<not_strong")


class Footnotes(Pattern):
    def __init__(self, pattern, config):
        super(Footnotes, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        identifier = m.group("identifier")
        text = m.group("text")
        print(identifier, text)

        span = etree.Element("span")
        label = etree.SubElement(span, "label")
        label.set("for", "footnote-{}".format(identifier))
        label.set("class", "margin-toggle sidenote-number")
        input = etree.SubElement(span, "input")
        input.set("type", "checkbox")
        input.set("id", "footnote-{}".format(identifier))
        input.set("class", "margin-toggle")
        text_span = etree.SubElement(span, "span")
        text_span.set("class", "sidenote")
        text_span.text = text

        return span


def makeExtension(*args, **kwargs):
    """Return extension."""

    return FootnoteExtension(*args, **kwargs)
