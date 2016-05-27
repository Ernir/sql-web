from markdown import markdown


def apply_markdown(md_text, section_id):
    """
    Applies Python's Markdown to the given text string, with the extensions required by the site.
    """
    # Deferred import due to circular logic
    from sql_web.markdown_extensions.internal_links import InternalLinkExtension
    from sql_web.markdown_extensions.footnotes import FootnoteExtension
    from sql_web.markdown_extensions.figures import FigureExtension
    return markdown(md_text, extensions=[
        InternalLinkExtension(),
        FootnoteExtension(section=section_id),
        FigureExtension(),
        "tables"
    ])
