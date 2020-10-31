import json

from django.core.management.base import BaseCommand
from locations.models import OwnerId, CalcAttribute, Point, Polygon, Object


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('odh_prepared.json') as data_file:
            data = json.load(data_file)

        for entry in data:
            owner_id_entry = entry.get('owner_id')
            print(owner_id_entry)
            owner_id = OwnerId.objects.create(
                legal_person_id=owner_id_entry.get('legal_person_id'),
                legal_person_version_id=owner_id_entry.get('legal_person_version_id'),
                start_date=owner_id_entry.get('start_date'),
                end_date=owner_id_entry.get('end_date')
            )
            owner_id.save()

            calc_attribute_entry = entry.get('calc_attribute')
            print(calc_attribute_entry)
            calc_attribute = CalcAttribute.objects.create(
                info=calc_attribute_entry.get('info', 0),
                sign=calc_attribute_entry.get('sign', 0),
                buffer=calc_attribute_entry.get('buffer', 0),
                pointer=calc_attribute_entry.get('pointer', 0),
                asperity=calc_attribute_entry.get('asperity', 0),
                tpu_area=calc_attribute_entry.get('tpu_area', 0),
                engin_qty=calc_attribute_entry.get('engin_qty', 0),
                other_area=calc_attribute_entry.get('other_area', 0),
                total_area=calc_attribute_entry.get('total_area', 0),
                guiding_qty=calc_attribute_entry.get('guiding_area', 0),
                margin_area=calc_attribute_entry.get('margin_area', 0),
                station_qty=calc_attribute_entry.get('station_qty', 0),
                bicycle_area=calc_attribute_entry.get('bicycle_area', 0),
                footway_area=calc_attribute_entry.get('footway_area', 0),
                guiding_area=calc_attribute_entry.get('guiding_area', 0),
                inbound_area=calc_attribute_entry.get('inbound_area', 0),
                roadway_area=calc_attribute_entry.get('roadway_area', 0),
                station_area=calc_attribute_entry.get('station_area', 0),
                bar_antinoise=calc_attribute_entry.get('bar_antinoise', 0),
                cleaning_area=calc_attribute_entry.get('cleaning_area', 0),
                bar_new_jersey=calc_attribute_entry.get('bar_new_jersey', 0),
                bicycle_length=calc_attribute_entry.get('bicycle_length', 0),
                guiding_length=calc_attribute_entry.get('guiding_length', 0),
                gutters_length=calc_attribute_entry.get('gutters_length', 0),
                station_number=calc_attribute_entry.get('station_number', 0),
                traff_light_qty=calc_attribute_entry.get('traff_light_qty', 0),
                auto_footway_area=calc_attribute_entry.get('auto_footway_area', 0),
                traffic_signs_qty=calc_attribute_entry.get('traffic_signs_qty', 0),
                tram_rails_length=calc_attribute_entry.get('tram_rails_length', 0),
                bound_stone_length=calc_attribute_entry.get('bound_stone_length', 0),
                manual_footway_area=calc_attribute_entry.get('manual_footway_area', 0),
                cleaning_guiding_qty=calc_attribute_entry.get('cleaning_guiding_qty', 0),
                cleaning_guiding_length=calc_attribute_entry.get('cleaning_guiding_length', 0),
                roadway_prkg_auto_clean_area=calc_attribute_entry.get('roadway_prkg_auto_clean_area', 0),
                roadway_noprkg_auto_clean_area=calc_attribute_entry.get('roadway_noprkg_auto_clean_area', 0),
                roadway_prkg_manual_clean_area=calc_attribute_entry.get('roadway_prkg_manual_clean_area', 0),
                roadway_noprkg_manual_clean_area=calc_attribute_entry.get('roadway_noprkg_manual_clean_area', 0)
            )
            calc_attribute.save()

            points = []
            for coordinates in entry.get('geometry').get('coordinates')[0]:
                point = Point.objects.create(
                    coordinates=f'{coordinates[0]};{coordinates[1]}'
                )
                point.save()
                points.append(point)

            polygon = Polygon.objects.create()
            polygon.points.set(points)
            polygon.save()

            _object = Object.objects.create(
                name=entry.get('name'),
                owner_id=owner_id,
                calc_attribute=calc_attribute,
            )
            _object.geometry.set([polygon, ])
            _object.save()
