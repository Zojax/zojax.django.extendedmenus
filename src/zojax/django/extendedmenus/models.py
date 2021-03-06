from django.db import models
from treemenus.models import MenuItem
    
    
class MenuItemExtension(models.Model):
    
    menu_item = models.OneToOneField (MenuItem, related_name="extension")
    selected_patterns = models.TextField(blank=True)
    only_anonymous = models.BooleanField(default=False)
    only_authenticated = models.BooleanField(default=False)    