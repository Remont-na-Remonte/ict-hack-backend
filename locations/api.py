from rest_framework import generics

from locations.serializers import ObjectSerializer
from locations.models import Object


class ObjectListAPI(generics.ListAPIView):
    serializer_class = ObjectSerializer

    def get_queryset(self):
        page = self.request.query_params.get('page', None)

        if page and page.isdigit() and int(page) > 0:
            return Object.objects.exclude(items__isnull=True)[(int(page) - 1) * 100:int(page) * 100]

        return Object.objects.exclude(items__isnull=True)
