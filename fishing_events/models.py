from django.db import models
from django.core import serializers
import json


class FishingEvent(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=200)
    location_details = models.TextField(blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    air_temp = models.IntegerField(blank=True, null=True)
    water_temp = models.IntegerField(blank=True, null=True)
    persons = models.IntegerField(blank=True, null=True)
    weather = models.CharField(max_length=200, blank=True)
    wind = models.IntegerField(blank=True, null=True)

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

    def get_all_events_and_catches(self):
        query_set = FishingEvent.objects.all()
        # order those events by date starting from latest date added
        ordered_set = query_set.order_by('-date')
        dict_data_raw = json.loads(serializers.serialize('json', ordered_set))
        ids = [obj['pk'] for obj in dict_data_raw]
        fc = FishCatch()
        fish_catches = fc.get_catches_by_event(ids)
        parsed_events = []
        for obj in dict_data_raw:
            catches = []
            for catch_obj in fish_catches:
                if obj['pk'] == catch_obj['fishing_event']:
                    catches.append(catch_obj)

            obj['fields']['catches'] = catches
            obj['fields']['id'] = obj['pk']
            parsed_events.append(obj['fields'])

        return parsed_events

    def get_all_events_and_catches_count(self):
        query_set = FishingEvent.objects.raw('SELECT fishing_events_fishingevent.*, COUNT(fishing_events_fishcatch.fishing_event_id) AS fish_count '
                                             'FROM fishing_events_fishingevent '
                                             'LEFT JOIN fishing_events_fishcatch '
                                             'ON (fishing_events_fishingevent.id = fishing_events_fishcatch.fishing_event_id) '
                                             'GROUP BY fishing_events_fishingevent.id')
        # Serializing will exclude fish_count field because it's not part of FishingEvent object
        dict_data_raw = json.loads(serializers.serialize('json', query_set))
        parsed_data = []
        for i, obj in enumerate(dict_data_raw):
            # this looks bit hacky but go with it until time to find better solution
            # add fish_count to parsed object
            obj['fields']['fish_count'] = query_set[i].fish_count
            obj['fields']['id'] = obj['pk']
            parsed_data.append(obj['fields'])

        return parsed_data

    def create_event(self, data):
        """
        :param data: dictionary object
        :return: id type integer of inserted object
        """
        fe = FishingEvent.objects.create(**data)
        obj_id = getattr(fe, 'pk')
        return obj_id

    def delete_event(self, pk):
        r = FishingEvent.objects.filter(pk=pk).delete()
        return r

class FishCatch(models.Model):
    fishing_event = models.ForeignKey(FishingEvent, related_name='fishing_event', on_delete=models.CASCADE)
    fish_species = models.CharField(max_length=100)
    weight = models.FloatField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    fishing_technique = models.CharField(max_length=100, blank=True)
    fishing_technique_details = models.TextField(blank=True)
    lure = models.CharField(max_length=100, blank=True)
    lure_details = models.TextField(blank=True)

    def get_catches_by_event(self, pk):
        """
        if using integer, it will query only one event
        Else queries using IN clause
        :param pk: either integer or list of integers
        :return: list of fish catches in dict
        """
        if isinstance(pk, int):
            query_set = FishCatch.objects.filter(fishing_event_id=pk)
        else:
            query_set = FishCatch.objects.filter(fishing_event_id__in=pk)
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
