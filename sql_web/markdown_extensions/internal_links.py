from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import re


def build_url(label, base, end):
    """ Build a url from the label, a base, and an end. """
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', label)
    return '%s%s%s' % (base, clean_label, end)


class InternalLinkExtension(Extension):
    """
    A Markdown extension for internal links heavily based on the SemanticWikiLinks Extension:
    https://github.com/aleray/mdx_semanticwikilinks
    """

    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url': ['/', 'String to append to beginning or URL.'],
            'end_url': ['/', 'String to append to end of URL.'],
            'html_class': ['wikilink', 'CSS hook. Leave blank for none.'],
            'build_url': [build_url, 'Callable formats URL from label.'],
        }

        super(InternalLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        INTERNALLINK_RE = r'(s?)\[\[([\w0-9_ -]+)\]\]'
        internal_link_pattern = InternalLinks(INTERNALLINK_RE, self.getConfigs())
        internal_link_pattern.md = md
        md.inlinePatterns.add('wikilink', internal_link_pattern, "<not_strong")


class InternalLinks(Pattern):
    def __init__(self, pattern, config):
        super(InternalLinks, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        if m.group(3).strip():
            if m.group(2) == "s":  # If the pattern is prefixed with "s", it's a section link
                self.config["base_url"] = "/vidfangsefni/"
            base_url, end_url, html_class = self._getConfig()
            label = m.group(3).strip()
            url = self.config['build_url'](label, base_url, end_url)
            a = etree.Element('a')
            a.text = label
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        else:
            a = ''
        return a

    def _getConfig(self):
        """ Return config data. """
        base_url = self.config['base_url']
        end_url = self.config['end_url']
        html_class = self.config['html_class']
        return base_url, end_url, html_class


def makeExtension(*args, **kwargs):
    return InternalLinkExtension(*args, **kwargs)
