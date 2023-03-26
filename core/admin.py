from django.contrib import admin

# Register your models here.

from .models import CustomUser, UserActivities

admin.site.register((CustomUser, UserActivities,))
