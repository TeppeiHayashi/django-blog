from django import template
from django.utils.safestring import mark_safe
import markdown  # @UnresolvedImport
from markdownx.utils import markdownify  # @UnresolvedImport
from markdownx.settings import (
    MARKDOWNX_MARKDOWN_EXTENSIONS,  # @UnresolvedImport
    MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS  # @UnresolvedImport
)
from markdown.extensions import Extension  # @UnresolvedImport

register = template.Library()


@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する。"""
    return mark_safe(markdownify(text))


class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):
    """マークダウンをhtmlに変換する。

    生のHTMLやCSS、JavaScript等のコードをエスケープした上で、マークダウンをHTMLに変換します。
    公開しているコメント欄等には、こちらを使ってください。

    """
    extensions = MARKDOWNX_MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions, extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)
    return mark_safe(html)

@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)

@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータの一部を置き換える。"""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()

@register.simple_tag
def title(subtitle = None):
    title = 'Blog'
    return title if not subtitle else f'{title} | {subtitle}'
    
    