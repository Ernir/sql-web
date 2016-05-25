from bs4 import BeautifulSoup
from markdown import markdown


def apply_markdown(md_text):
    """
    Applies Python's Markdown to the given text string, with the extensions required by the site.
    """
    # Deferred import due to circular logic
    from sql_web.markdown_extensions.internal_links import InternalLinkExtension
    return markdown(md_text, extensions=[InternalLinkExtension(), "footnotes", "tables"])


def clean_footnotes(original_html):
    """
    Post-processes a given HTML string, assumed to be generated by Markdown, to comply with the site's demands.
    """
    soup = BeautifulSoup(original_html, "html.parser")
    footnote_container = soup.find_all("div", class_="footnote")

    for footnote in soup.find_all("a", class_="footnote-ref"):
        whole_reference = footnote.parent
        reference_id = footnote.get("href")[1:]

        footnote_content_list = [element for element in soup.find(id=reference_id).strings]
        footnote_contents = "".join(footnote_content_list)
        tufte_footnote = '<label for="{0}" class="margin-toggle sidenote-number"></label><input type="checkbox" id="{0}" class="margin-toggle"><span class="sidenote">{1}</span> '.format(
            reference_id, footnote_contents)
        whole_reference.replace_with(BeautifulSoup(tufte_footnote, "html.parser"))

    for element in footnote_container:
        element.extract()

    return str(soup)
