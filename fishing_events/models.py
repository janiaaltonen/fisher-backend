from django.db import models
from django.core import serializers
import json


class FishingEvent(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=200)
    location_details = models.TextField(blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    air_temp = models.IntegerField(blank=True)
    water_temp = models.IntegerField(blank=True)
    persons = models.IntegerField(blank=True)
    weather = models.CharField(max_length=200, blank=True)
    wind = models.IntegerField(blank=True)

    def get_event_by_pk(self, pk):
        query_set = FishingEvent.objects.filter(pk=pk)
        dict_data = json.loads(serializers.serialize('json', query_set))
        return dict_data[0]['fields']   # Return only fields and not 'pk' and 'model'

    def get_full_event(self, pk):
        fishing_event = self.get_event_by_pk(pk)
        fc = FishCatch()
        catches = fc.get_catches_by_event(pk)
        fishing_event['catches'] = catches

        return fishing_event

    def get_all_events_and_catches_count(self):
        query_set = FishingEvent.objects.raw('SELECT fishing_events_fishingevent.*, COUNT(fishing_events_fishcatch.fishing_event_id) AS fish_count '
                                             'FROM fishing_events_fishingevent '
                                             'LEFT JOIN fishing_events_fishcatch '
                                             'ON (fishing_events_fishingevent.id = fishing_events_fishcatch.fishing_event_id) '
                                             'GROUP BY fishing_events_fishingevent.id')
        dict_data_raw = json.loads(serializers.serialize('json', query_set))
        parsed_data = []
        for obj in dict_data_raw:
            obj['field']['id'] = obj['pk']
            parsed_data.append(obj)

        return parsed_data

    def create_event(self, data):
        """
        :param data: dictionary object
        :return: id type integer of inserted object
        """
        fe = FishingEvent.objects.create(**data)
        obj_id = getattr(fe, 'pk')
        return obj_id


class FishCatch(models.Model):
    fishing_event = models.ForeignKey(FishingEvent, related_name='fishing_event', on_delete=models.CASCADE)
    fish_species = models.CharField(max_length=100)
    weight = models.FloatField(blank=True)
    length = models.IntegerField(blank=True)
    fishing_technique = models.CharField(max_length=100, blank=True)
    fishing_technique_details = models.TextField(blank=True)
    lure = models.CharField(max_length=100, blank=True)
    lure_details = models.TextField(blank=True)

    def get_catches_by_event(self, pk):
        query_set = FishCatch.objects.filter(pk=pk)
        dict_data = json.loads(serializers.serialize('json', query_set))
        catches = []
        for obj in dict_data:
            obj['fields']['id'] = obj['pk']
            catches.append(obj['fields'])

        return catches

    def bulk_create_catches(self, catches_data):
        """
        :param catches_data: list of fish_catch objects
        :return : now it just returns the inserted objects without ids (bulk)
        """
        catches = [FishCatch(**data) for data in catches_data]
        objs = FishCatch.objects.bulk_create(catches)
        return objs


class FishSpecies(models.Model):
    name = models.CharField(max_length=100)

    def get_all(self):
        query_set = FishSpecies.objects.all()
        dict_data = json.loads(serializers.serialize('json', query_set))
        fish_species = []

        for obj in dict_data:
            fish_species.append(obj['fields'])

        return fish_species


class WeatherOption(models.Model):
    name = models.CharField(max_length=100)

    def get_all(self):
        query_set = WeatherOption.objects.all()
        dict_data = json.loads(serializers.serialize('json', query_set))
        options = []

        for obj in dict_data:
            options.append(obj['fields'])

        return options


class Lure(models.Model):
    name = models.CharField(max_length=100)

    def get_all(self):
        query_set = Lure.objects.all()
        dict_data = json.loads(serializers.serialize('json', query_set))
        options = []

        for obj in dict_data:
            options.append(obj['fields'])

        return options


class FishingTechnique(models.Model):
    name = models.CharField(max_length=100)

    def get_all(self):
        query_set = FishingTechnique.objects.all()
        dict_data = json.loads(serializers.serialize('json', query_set))
        options = []

        for obj in dict_data:
            options.append(obj['fields'])

        return options
