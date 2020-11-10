from django.urls import path

from locations.api import ObjectListAPI, CloseObjectsListAPI


urlpatterns = [
    path('api/objects/all', ObjectListAPI.as_view(), name='objects-all'),
    path('api/objects/closest', CloseObjectsListAPI.as_view(), name='objects-closest')
]
