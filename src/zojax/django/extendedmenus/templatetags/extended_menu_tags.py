from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from treemenus.models import MenuItem
import re
from zojax.django.extendedmenus.models import MenuItemExtension


register = template.Library()


@register.filter
def displayed_menu_items(menu_items, request):
    user = request.user
    children = []
    for child in menu_items:
        try:
            extension = child.extension
            if user.is_anonymous() and extension.only_authenticated:
                continue
            if user.is_authenticated() and extension.only_anonymous:
                continue
        except MenuItemExtension.DoesNotExist:
            pass
        children.append(child)
    for i, child in enumerate(children):
        child.next = None
        child.previous = None
        try:
            child.next = children[i+1]
        except IndexError:
            pass
        try:
            child.previous = children[i-1]
        except IndexError:
            pass
         
    return children


@register.filter
def menu_item_selected(menu_item, request):
    if not isinstance(menu_item, MenuItem):
        return False
    try:
        selected_patterns = menu_item.extension.selected_patterns
        for pattern in selected_patterns.splitlines():
            if selected_patterns and re.compile(pattern).match(request.path):
                return True
    except MenuItemExtension.DoesNotExist:
            pass

    if menu_item.named_url:
        try:
            url = reverse(menu_item.named_url)
        except NoReverseMatch:
            url = '#'
    else:
        url = menu_item.url

    if request.path == url:
        return True

    return False


@register.filter
def menu_item_have_selected(menu_item, request):
    if not isinstance(menu_item, MenuItem):
        return False

    for child in menu_item.children():
        if menu_item_selected(child, request):
            return True

    return False

    
class ReverseNamedURLNode(Node):
    def __init__(self, named_url, parser):
        self.named_url = named_url
        self.parser = parser

    def render(self, context):
        from django.template import TOKEN_BLOCK, Token
        
        resolved_named_url = self.named_url.resolve(context)
        contents = u'url ' + resolved_named_url
        
        urlNode = url(self.parser, Token(token_type=TOKEN_BLOCK, contents=contents))
        try:
            return urlNode.render(context)
        except NoReverseMatch:
            return '#'


@register.tag
def reverse_named_url(parser, token):
    bits = token.contents.split(' ', 2)
    if len(bits) !=2 :
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (named url)" % bits[0])
    named_url = parser.compile_filter(bits[1])
    
    return ReverseNamedURLNode(named_url, parser)
