from rest_framework import serializers

from itemized_lists.models import Item, ItemizedList


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class ItemizedListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = ItemizedList
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    year = serializers.IntegerField()

    class Meta:
        fields = ('file', 'year', )
