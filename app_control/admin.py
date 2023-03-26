from django.contrib import admin
from .models import InventoryGroup, InventoryItem


admin.site.register((InventoryItem, InventoryGroup,))
