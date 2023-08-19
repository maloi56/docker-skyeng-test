import base64

from django import template
from pygments import highlight, lexers
from pygments.formatters.img import ImageFormatter
from pygments.styles import get_style_by_name

register = template.Library()


def image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')


@register.filter(name='highlight')
def highlight_code(value):
    lexer = lexers.get_lexer_by_name('python')
    style = get_style_by_name('native')
    formatter = ImageFormatter(full=True, style=style)
    highlighted_code = highlight(value, lexer, formatter)
    return image_to_base64(highlighted_code)


@register.filter(name='decode_utf8')
def decode_utf8(value):
    return value.decode('utf-8')
