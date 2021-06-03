from django.contrib import admin
from .models import FishingEvent, FishingTechnique, FishCatch, FishSpecies, WeatherOption, Lure

admin.site.register(FishingEvent)
admin.site.register(FishCatch)
admin.site.register(FishSpecies)
admin.site.register(WeatherOption)
admin.site.register(Lure)
admin.site.register(FishingTechnique)
