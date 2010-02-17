from django import template
from django.core.urlresolvers import reverse
from treemenus.models import MenuItem
import re


register = template.Library()


def displayed_menu_items(menu_items, request):
    user = request.user
    children = []
    for child in menu_items:
        if user.is_anonymous() and child.extension.only_authenticated:
            continue
        if user.is_authenticated() and child.extension.only_anonymous:
            continue
        children.append(child)
    return children
    
register.filter('displayed_menu_items', displayed_menu_items)


def menu_item_selected(menu_item, request):
    if not isinstance(menu_item, MenuItem):
        return False
    selected_patterns = menu_item.extension.selected_patterns
    for pattern in selected_patterns.splitlines():
        if selected_patterns and re.compile(pattern).match(request.path):
            return True
        
    if menu_item.named_url:
        url = reverse(menu_item.named_url) 
    else:
        url = menu_item.url

    if request.path == url:
        return True
        
    return False

register.filter('menu_item_selected', menu_item_selected)
