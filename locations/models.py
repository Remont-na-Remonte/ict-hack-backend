from django.db import models
from location_field.models.plain import PlainLocationField


class OwnerId(models.Model):
    legal_person_id = models.BigIntegerField()
    legal_person_version_id = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class CalcAttribute(models.Model):
    info = models.FloatField(default=0.0, blank=True)
    sign = models.FloatField(default=0.0, blank=True)
    buffer = models.FloatField(default=0.0, blank=True)
    pointer = models.FloatField(default=0.0, blank=True)
    asperity = models.FloatField(default=0.0, blank=True)
    tpu_area = models.FloatField(default=0.0, blank=True)
    engin_qty = models.IntegerField(default=0, blank=True)
    other_area = models.FloatField(default=0.0, blank=True)
    total_area = models.FloatField(default=0.0, blank=True)
    guiding_qty = models.IntegerField(default=0, blank=True)
    margin_area = models.FloatField(default=0.0, blank=True)
    station_qty = models.IntegerField(default=0, blank=True)
    bicycle_area = models.FloatField(default=0.0, blank=True)
    footway_area = models.FloatField(default=0.0, blank=True)
    guiding_area = models.FloatField(default=0.0, blank=True)
    inbound_area = models.FloatField(default=0.0, blank=True)
    roadway_area = models.FloatField(default=0.0, blank=True)
    station_area = models.FloatField(default=0.0, blank=True)
    bar_antinoise = models.FloatField(default=0.0, blank=True)
    cleaning_area = models.FloatField(default=0.0, blank=True)
    bar_new_jersey = models.FloatField(default=0.0, blank=True)
    bicycle_length = models.FloatField(default=0.0, blank=True)
    guiding_length = models.FloatField(default=0.0, blank=True)
    gutters_length = models.FloatField(default=0.0, blank=True)
    station_number = models.IntegerField(default=0, blank=True)
    traff_light_qty = models.IntegerField(default=0, blank=True)
    auto_footway_area = models.FloatField(default=0.0, blank=True)
    traffic_signs_qty = models.IntegerField(default=0, blank=True)
    tram_rails_length = models.FloatField(default=0.0, blank=True)
    bound_stone_length = models.FloatField(default=0.0, blank=True)
    manual_footway_area = models.FloatField(default=0.0, blank=True)
    cleaning_guiding_qty = models.IntegerField(default=0, blank=True)
    cleaning_guiding_length = models.FloatField(default=0.0, blank=True)
    roadway_prkg_auto_clean_area = models.FloatField(default=0.0, blank=True)
    roadway_noprkg_auto_clean_area = models.FloatField(default=0.0, blank=True)
    roadway_prkg_manual_clean_area = models.FloatField(default=0.0, blank=True)
    roadway_noprkg_manual_clean_area = models.FloatField(default=0.0, blank=True)


class Point(models.Model):
    coordinates = PlainLocationField(zoom=7)

    def __str__(self):
        return f'Point {self.coordinates}'


class Polygon(models.Model):
    points = models.ManyToManyField(Point)

    def __str__(self):
        return f'Polygon #{self.pk}'


class Object(models.Model):
    name = models.CharField(max_length=512)
    owner_id = models.ForeignKey(OwnerId, related_name='_objects', on_delete=models.CASCADE)
    calc_attribute = models.ForeignKey(CalcAttribute, related_name='_objects', on_delete=models.CASCADE)
    geometry = models.ManyToManyField(Polygon)

    def __str__(self):
        return self.name
