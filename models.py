from django.db import models
from location_field.models.plain import PlainLocationField

class Inspector(models.Model):
    score = models.IntegerField(default=0, blank=True)
    photo_link = models.TextField()
    comment = models.TextField()
    inspector_id = models.IntegerField()
