#from datetime import date as dt
from datetime import datetime
from decimal import Decimal
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
                date = datetime(int(budget_entry['budgetFunds']['stages'][0]['payments']['paymentYear']),
                        int(budget_entry['budgetFunds']['stages'][0]['payments']['paymentMonth']), 1)
                
                budget = Budget.objects.get_or_create(
                    code=budget_entry['budget']['code'] != 'null' or 0.0,
                    endDate = datetime.fromisoformat(budget_entry['budgetFunds']['stages'][0]['endDate'][:-1]),
                    KBK = Decimal(budget_entry['budgetFunds']['stages'][0]['payments']['KBK']),
                    paymentSumRUR=float(budget_entry.get('budgetFunds').get('stages')[0].get('payments').get('paymentSumRUR')) != 'null' or 0.0,
                    name=budget_entry['budget']['name'],
                    paymentYearMonth=date
                )

                contract_entry = entry.get('contract')
                print(contract_entry['scan'][0]['url'])
                contract = Contract.objects.create(
                    id=str(contract_entry['_id']),
                    contractUrl=str(contract_entry['contractUrl']) != 'null' or 0.0,
                    documentBase=str(contract_entry['documentBase']) != 'null' or 0.0,
                    startDate=datetime.fromisoformat(contract_entry['execution']['startDate'][:-1]),
                    endDate=datetime.fromisoformat(contract_entry['execution']['endDate'][:-1]),
                    fz=int(contract_entry['fz']) != 'null' or 0.0,
                    price=Decimal(contract_entry['price']) != 'null' or 0.0,
                    printFromUrl=str(contract_entry['printFormUrl']) != 'null' or 0.0,
                    protocolDate=datetime.fromisoformat(contract_entry['protocolDate']) != 'null' or 0.0,
                    publishDate=datetime.fromisoformat(contract_entry['publishDate']) != 'null' or 0.0,
                    signDate=datetime.fromisoformat(contract_entry['signDate'][:-1]), 
                    regionCode=int(contract_entry['regionCode']) != 'null' or 0.0,
                    scanUrl=str(contract_entry['scan'][0]['url']))
                contract.budget.set(budget)
                contract.save()
                print('+++++++++++++++++++++++++++++++++++++++')
                object = Object.objects.get_or_create(
                    id=entry.get('_id'),
                    title=entry.get('title') != 'null' or 0.0,
                    region=entry.get('region') != 'null' or 0.0,
                    signDate=datetime.strptime(entry.get('signDate'),"%Y-%m-%d") != 'null' or 0.0,
                    contract=str(contract)
                )

                # product_entry = data['contract']['products']
                # for product in product_entry:
