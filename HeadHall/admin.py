from django.contrib import admin
from .models import ELevel, DLevel, CLevel, BLevel


@admin.register(ELevel, DLevel, CLevel, BLevel)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('OBJECTID',
                    'PlaceName', 'PersonName', 'Contact', 'Email', 'Details',
                    'PlaceNode', 'PlaceType')
