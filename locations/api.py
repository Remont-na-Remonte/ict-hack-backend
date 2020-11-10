from rest_framework import generics, status
from rest_framework.response import Response
from scipy import spatial

from locations.serializers import ObjectSerializer
from locations.models import Object


class ObjectListAPI(generics.ListAPIView):
    serializer_class = ObjectSerializer

    def get_queryset(self):
        params = self.request.query_params
        page = params.get('page', None)
        queryset = Object.objects.exclude(items__isnull=True)

        if page and page.isdigit() and int(page) > 0:
            queryset = queryset[(int(page) - 1) * 100:int(page) * 100]

        return queryset


class CloseObjectsListAPI(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        params = self.request.query_params
        page = params.get('page', None)
        queryset = Object.objects.exclude(items__isnull=True)

        if page and page.isdigit() and int(page) > 0:
            queryset = queryset[(int(page) - 1) * 100:int(page) * 100]

        if 'lat' in params and 'long' in params:
            coordinates = []
            objects = []
            for _object in queryset:
                polygon = _object.geometry.first()
                coordinates.append(tuple(map(lambda item: float(item), polygon.points.first().coordinates.split(';'))))
                objects.append(_object)

            user_location = (float(params.get('lat')), float(params.get('long')))
            tree = spatial.KDTree(coordinates)
            close_points_ids = tree.query_ball_point(user_location, 2000)

            queryset = []
            for _id in close_points_ids:
                object_dict = {
                    'name': objects[_id].name,
                    'lat': coordinates[_id][0],
                    'long': coordinates[_id][1]
                }
                queryset.append(object_dict)

        response_dict = {
            "objects": queryset,
        }

        return Response(response_dict, status=status.HTTP_200_OK)
