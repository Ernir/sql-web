from django.core.exceptions import ObjectDoesNotExist
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
from sql_web.models import Section, Figure


class InternalLinkExtension(Extension):
    """
    A Markdown extension for internal links based on the SemanticWikiLinks Extension:
    https://github.com/aleray/mdx_semanticwikilinks

    Links handled by this extension take one of two formats. The first format is:

    [[identifier|label]]

    Where identifier is the unique identifier of a section or other entity with a defined URL.
    Label is the text that will be displayed in the rendered document.

    The other format is:

    [[identifier]]

    Where identifier is as before, but label = identifier is assumed.
    """

    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url': ['/', 'String to append to beginning or URL.'],
            'end_url': ['/', 'String to append to end of URL.'],
            'html_class': ['internal-link', 'CSS hook. Leave blank for none.'],
        }

        super(InternalLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        INTERNALLINK_RE = r'\[\[(?P<all_contents>(?P<identifier>[a-z\d#-_]+)(?P<sep>\|?)(?P<label>.*?))\]\]'
        internal_link_pattern = InternalLinks(INTERNALLINK_RE, self.getConfigs())
        internal_link_pattern.md = md
        md.inlinePatterns.add('internallink', internal_link_pattern, "<not_strong")


class InternalLinks(Pattern):
    def __init__(self, pattern, config):
        super(InternalLinks, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        identifier = m.group("identifier")
        if not m.group("sep"):
            label = identifier
        else:
            label = m.group("label")

        url = self.get_url_from_identifier(identifier)

        a = etree.Element('a')
        a.text = label
        a.set('href', url)
        if self.config["html_class"]:
            a.set('class', self.config["html_class"])
        return a

    def get_url_from_identifier(self, identifier):
        section = None
        try:
            section = Section.objects.get(identifier=identifier)
        except ObjectDoesNotExist:
            pass
        figure = None
        try:
            figure = Figure.objects.get(identifier=identifier)
        except ObjectDoesNotExist:
            pass

        if section:
            url = section.get_absolute_url()
        elif figure:
            url = figure.image.url
        else:
            url = "/{}/".format(identifier)

        return url


def makeExtension(*args, **kwargs):
    return InternalLinkExtension(*args, **kwargs)
