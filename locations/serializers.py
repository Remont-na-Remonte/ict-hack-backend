from rest_framework import serializers

from locations.models import OwnerId, CalcAttribute, Point, Polygon, Object


class OwnerIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = OwnerId
        fields = '__all__'


class CalcAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalcAttribute
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('coordinates', )


class PolygonSerializer(serializers.ModelSerializer):
    points = PointSerializer(read_only=True, many=True)

    class Meta:
        model = Polygon
        fields = ('points', )


class ObjectSerializer(serializers.ModelSerializer):
    geometry = PolygonSerializer(read_only=True, many=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'geometry', )
