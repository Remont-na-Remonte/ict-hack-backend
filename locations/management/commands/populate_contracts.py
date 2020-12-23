from datetime import datetime
from backports.datetime_fromisoformat import MonkeyPatch
import bigjson
from django.core.management.base import BaseCommand

from contracts.models import Object, Contract, Budget, Product, Contract_Customer, Contract_Supplier, Customer, Supplier, Section, Road, Section_Road
MonkeyPatch.patch_fromisoformat()

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('full_export.json', 'rb') as json_file:
            data = bigjson.load(json_file)
            for entry in data:
                budget_entry = (entry.get('contract')).get('finances')
                _budget = Budget.objects.create(
                    code=budget_entry['budget']['code'],
                    name=budget_entry['budget']['name'],

                    paymentYearMonth=datetime(int(budget_entry['budgetFunds']['stages'][0]['payments']['paymentYear']),
                        int(budget_entry['budgetFunds']['stages'][0]['payments']['paymentMonth']), 1),
                    paymentSumRUR=budget_entry['budgetFunds']['stages'][0]['payments']['paymentSumRUR']
                )
                budget.save()

                print(dir(budget[0]))
                contract_entry = entry.get('contract')
                contract = Contract.objects.get_or_create(
                    id=contract_entry['_id'],
                    contractUrl=contract_entry['contractUrl'],
                    documentBase=contract_entry['documentBase'],
                    startDate=contract_entry['execution']['startDate'],
                    endDate=contract_entry['execution']['endDate'],
                    fz=contract_entry['fz'],
                    price=contract_entry['price'],
                    printFormUrl=contract_entry['printFormUrl'],
                    protocolDate=datetime.fromisoformat(contract_entry['protocolDate']),
                    publichDate=datetime.fromisoformat(contract_entry['publishDate']),
                    regionCode=contract_entry['regionCode'],
                    scanUrl=contract_entry['scan'][0]['url'],
                    signDate=contract_entry['signDate'],
                    budget=_budget
                )

                object = Object.objects.get_or_create(
                    id=entry.get('_id'),
                    title=entry.get('title'),
                    region=entry.get('region'),
                    signDate=datetime.strptime(entry.get('signDate'),"%Y-%m-%d"),
                    contract=contract
                )

                # product_entry = data['contract']['products']
                # for product in product_entry:
