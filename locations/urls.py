from django.urls import path

from locations.api import ObjectListAPI


urlpatterns = [
    path('api/objects/all', ObjectListAPI.as_view(), name='objects-all'),
]
