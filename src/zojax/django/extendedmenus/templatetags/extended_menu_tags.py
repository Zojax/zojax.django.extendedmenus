from django import template
from django.core.urlresolvers import reverse
from treemenus.models import MenuItem
import re
from zojax.django.extendedmenus.models import MenuItemExtension


register = template.Library()


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

register.filter('displayed_menu_items', displayed_menu_items)


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
        url = reverse(menu_item.named_url)
    else:
        url = menu_item.url

    if request.path == url:
        return True

    return False

register.filter('menu_item_selected', menu_item_selected)
