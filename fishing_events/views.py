from django.views import View
from django.http import HttpResponse
from .models import FishingEvent, FishingTechnique, FishCatch, FishSpecies, WeatherOption, Lure
import json
from .utils import parse_request_payload


class FullEvent(View):

    def get(self, request):
        fe = FishingEvent()
        fishing_event = fe.get_full_event(1)
        return HttpResponse(json.dumps(fishing_event), content_type='application/json')


class AllEvents(View):

    def get(self, request):
        fe = FishingEvent()
        events = fe.get_all_events_and_catches()
        return HttpResponse(json.dumps(events), content_type='application/json')


class CreateEvent(View):

    def post(self, request):
        print(request.body)
        event, catches = parse_request_payload(request.body)
        fe = FishingEvent()
        event_id = fe.create_event(event)
        fc = FishCatch()
        for c in catches:
            c['fishing_event_id'] = event_id
        fish_catch_objs = fc.bulk_create_catches(catches)
        print('fish catch objs')
        print(fish_catch_objs)

        return HttpResponse(json.dumps({'message': 'ok'}), status=201, content_type='application/json')

class DeleteEvent(View):

    def delete(self, request):
        print(request.body)

        return HttpResponse(json.dumps({'message': 'ok'}), status=200, content_type='application/json')


class Fish(View):

    def get(self, request):
        fs = FishSpecies()
        fish_species = fs.get_all()
        return HttpResponse(json.dumps(fish_species), status=200, content_type='application/json')

class Weather(View):

    def get(self, request):
        wo = WeatherOption()
        options = wo.get_all()
        return HttpResponse(json.dumps(options), status=200, content_type='application/json')


class Lures(View):

    def get(self, request):
        lure = Lure()
        lures = lure.get_all()
        return HttpResponse(json.dumps(lures), status=200, content_type='application/json')


class FishingTechniques(View):

    def get(self, reques):
        ft = FishingTechnique()
        fts = ft.get_all()
        return HttpResponse(json.dumps(fts), status=200, content_type='application/json')