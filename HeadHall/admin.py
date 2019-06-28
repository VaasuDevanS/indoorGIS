from django.contrib import admin
from .models import ELevel

@admin.register(ELevel)
class ELevelAdmin(admin.ModelAdmin):
    list_display = ('OBJECTID',
                    'PlaceName', 'PersonName', 'Contact', 'Email', 'Details',
                    'PlaceNode',)
