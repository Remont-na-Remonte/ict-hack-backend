#from datetime import date as dt
import django
import json
from datetime import datetime
from decimal import Decimal
from backports.datetime_fromisoformat import MonkeyPatch
import bigjson
from django.core.management.base import BaseCommand
from contracts.models import Object, Contract, Budget, Product, Contract_Customer, Contract_Supplier, Customer, Supplier, Section, Road, Section_Road
MonkeyPatch.patch_fromisoformat()


def try_to_date(date):
    try:
        return datetime.fromisoformat(date)
    except:
        return None


def try_get_first(_list):
    return next(iter(_list or []), None)


def try_get_get(value, to_get):
    try:
        return value.get(to_get)
    except:
        return None


def try_to_num(num, num_type):
    if num is None:
        return None

    if num_type == "int":
        return int(num)

    if num_type == "float":
        return float(num)

    if num_type == "decimal":
        return Decimal(num)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('parsed_dissected.json', 'rb') as json_file2: 
            data2 = bigjson.load(json_file2)['features']
            for entry in data2:
                coords = []
                for cor in entry.get('geometry').get('coordinates'):
                    xy = [cor[0], cor[1]]
                    coords.append(xy)

                sc = Section.objects.create(
                    km = try_to_num(entry.get('properties').get('km'), 'int'),
                    section_start = try_to_num(entry.get('properties').get('section_start'), 'int'),
                    section_end = try_to_num(entry.get('properties').get('section_end'), 'int'),
                    coordinates = json.dumps(list(coords))
                )

                contracts = entry['properties']['contract']
                for contract in contracts:
                    #print(contract.get('id'))
                    try:
                        ct = Contract.objects.get(id=contract.get('id'))
                        sc.contracts.add(ct)
                    except:
                        pass
                        #print('----------404 CONTRACT-------------***')
                sc.save()

                rd = Road.objects.create(
                    type = entry.get('geometry').get('type'),
                    road_title = entry.get('properties').get('road_title')
                )
                rd.sections.add(sc)
                rd.save()
