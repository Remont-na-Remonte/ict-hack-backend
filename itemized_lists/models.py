from django.db import models

from locations.models import Object


class Item(models.Model):
    name = models.CharField(max_length=512)
    start_position = models.CharField(max_length=256)
    end_position = models.CharField(max_length=256)
    district = models.CharField(max_length=64)
    justification = models.CharField(max_length=512)
    program = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    roadway_area = models.FloatField(default=0.0)
    footway_area = models.FloatField(default=0.0)
    margin_area = models.FloatField(default=0.0)
    total_area = models.FloatField(default=0.0)
    _object = models.ForeignKey(Object, related_name='items', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemizedList(models.Model):
    name = models.CharField(max_length=512)
    year = models.IntegerField(unique=True, primary_key=True)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name
