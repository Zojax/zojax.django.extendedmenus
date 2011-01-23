from treemenus.admin import MenuAdmin, MenuItemAdmin
from treemenus.models import Menu
from django.contrib import admin
from zojax.django.extendedmenus.models import MenuItemExtension


class MenuItemExtensionInline(admin.StackedInline):
    model = MenuItemExtension
    max_num = 1


class ExtendedMenuItemAdmin(MenuItemAdmin):
    inlines = [MenuItemExtensionInline,]


class ExtendedMenuAdmin(MenuAdmin):
    menu_item_admin_class = ExtendedMenuItemAdmin


admin.site.unregister(Menu)
admin.site.register(Menu, ExtendedMenuAdmin)

