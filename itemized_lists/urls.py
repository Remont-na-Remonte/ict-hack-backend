from django.urls import path

from itemized_lists.api import ItemizedListAPI, ItemizedListUploadAPI


urlpatterns = [
    path('api/itemized-list/<year>', ItemizedListAPI.as_view(), name='retrieve-itemized-list'),
    path('api/itemized-lists/upload', ItemizedListUploadAPI.as_view(), name='upload-itemized-list'),
]
