from django.contrib import admin

from locations.models import OwnerId, CalcAttribute, Point, Polygon, Object

admin.site.register(OwnerId)
admin.site.register(CalcAttribute)
admin.site.register(Point)
admin.site.register(Polygon)
admin.site.register(Object)
