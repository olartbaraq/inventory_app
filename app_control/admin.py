from django.contrib import admin
from .models import InventoryGroup, InventoryItem, Shop


admin.site.register((InventoryItem, InventoryGroup, Shop))
