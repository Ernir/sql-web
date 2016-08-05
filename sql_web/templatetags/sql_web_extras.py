from django import template

register = template.Library()


@register.inclusion_tag("snippets/marginnote.html")
def marginnote(marginnote_id, marginnote_contents):
    return {"marginnote_id": marginnote_id, "marginnote_contents": marginnote_contents}
