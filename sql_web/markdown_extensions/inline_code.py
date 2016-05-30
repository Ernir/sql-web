from markdown.util import etree
from markdown import Extension
from markdown.inlinepatterns import Pattern, BACKTICK_RE


class InlineCodeExtension(Extension):
    """
    A Markdown extension overriding the default handling of inline code to use the format used by tufte-css.
    Instead of wrapping inline code in <code> blocks, divs with .code are used.

    Syntax is unchanged.
    """

    def extendMarkdown(self, md, md_globals):
        backtick_pattern = InlineCode(BACKTICK_RE, self.getConfigs())
        backtick_pattern.md = md
        md.inlinePatterns['backtick'] = backtick_pattern


class InlineCode(Pattern):
    def __init__(self, pattern, config):
        self.config = config
        super(InlineCode, self).__init__(pattern)

    def handleMatch(self, m):
        span = etree.Element("span")
        span.set("class", "code")
        span.text = m.group(3)

        return span


def makeExtension(*args, **kwargs):
    """Return extension."""

    return InlineCodeExtension(*args, **kwargs)
