
#from django.contrib import admin
from django.contrib.gis import admin
from .models import Preferences, ChatMessage, Match

admin.site.register(Match, admin.GeoModelAdmin)
admin.site.register(Preferences, admin.GeoModelAdmin)
'''
admin.register(Geolocation)
admin.register(Prospect)
admin.register(Preferences)
admin.register(ChatMessage)
'''