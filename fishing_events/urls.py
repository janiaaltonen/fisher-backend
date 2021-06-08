from django.urls import path
from .views import FullEvent, AllEvents, CreateEvent, Fish, Weather, FishingTechniques, Lures

urlpatterns = [
    path('fullEvent', FullEvent.as_view()),
    path('allEvents', AllEvents.as_view()),
    path('createFishingEvent', CreateEvent.as_view()),
    path('fishSpecies', Fish.as_view()),
    path('weatherOptions', Weather.as_view()),
    path('lureOptions', Lures.as_view()),
    path('fishingTechniqueOptions', FishingTechniques.as_view())
]
