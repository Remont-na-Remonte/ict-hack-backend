import io, csv

from pandas import ExcelFile
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from itemized_lists.models import Item, ItemizedList
from itemized_lists.serializers import ItemizedListSerializer, FileUploadSerializer
from locations.models import Object


class ItemizedListAPI(generics.RetrieveAPIView):
    serializer_class = ItemizedListSerializer
    queryset = ItemizedList.objects.all()
    lookup_field = 'year'


class ItemizedListUploadAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        year = serializer.validated_data['year']
        file = serializer.validated_data['file']
        excel_data = ExcelFile(io.BytesIO(file.read()))
        dataframe = excel_data.parse()

        items = []
        for index, row in dataframe.iterrows():
            if index > 5:
                name = row[1]
                if name.startswith('Итого по округам'):
                    break

                name.replace('улица', '')
                name.replace('ул.', '')
                name.replace('ул', '')
                name.replace('переулок', '')
                name.replace('пер.', '')
                name.replace('пер', '')
                name.strip()

                matches = Object.objects.filter(name__contains=name)

                item = Item.objects.create(
                    name=row[1],
                    start_position=row[2],
                    end_position=row[3],
                    district=row[4],
                    justification=row[4],
                    program=row[6],
                    category=row[7],
                    roadway_area=float(row[8]),
                    footway_area=float(row[9]),
                    margin_area=float(row[10]),
                    total_area=float(row[11]),
                )
                if matches:
                    item._object = matches[0]
                item.save()
                items.append(item)

        name = str(file).split('.')[0]
        itemized_list = ItemizedList.objects.create(
            name=name,
            year=year
        )
        itemized_list.items.set(items)
        itemized_list.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
