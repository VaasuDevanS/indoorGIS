from django.contrib import admin
from .models import ELevel, DLevel, CLevel, BLevel, Stat


@admin.register(ELevel, DLevel, CLevel, BLevel)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('OBJECTID',
                    'PlaceName', 'PersonName', 'Contact', 'Email', 'Details',
                    'PlaceNode', 'PlaceType')


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'functionality', 'keyword', 'returned')
