#from datetime import date as dt
import django
from datetime import datetime
from decimal import Decimal
from backports.datetime_fromisoformat import MonkeyPatch
import bigjson
from django.core.management.base import BaseCommand
from contracts.models import Object, Contract, Budget, Product, Contract_Customer, Contract_Supplier, Customer, Supplier, Section, Road, Section_Road
MonkeyPatch.patch_fromisoformat()
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def log(mess, isOk=True):
    if isOk:
        print(bcolors.OKGREEN + "[+] " + mess + bcolors.ENDC)
    if not isOk:
        print(bcolors.FAIL + "[!] " + mess + bcolors.ENDC)

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('full_export.json', 'rb') as json_file, open('parsed_dissected.json', 'rb') as json_file2: 
            data = bigjson.load(json_file)
            count = 0
            for entry in data:
                budget_entry = None
                #if count < 129663:
                #    count += 1
                #    continue
                try:
                    budget_entry = (entry.get('contract')).get('finances')
                except:
                    log('Budget FUCKED UP', False)
                date = None
                try:
                    date = datetime(int(budget_entry['budgetFunds']['stages'][0]['payments']['paymentYear']),
                        int(budget_entry['budgetFunds']['stages'][0]['payments']['paymentMonth']), 1)
                except:
                    pass

                try:
                    budget_entry.get('budget').get('code')
                except:
                    log('Budget Fucked Up', False)
                    continue

                try:
                    bg = Budget.objects.create(
                        code=budget_entry.get('budget').get('code'),
                        endDate = try_to_date(budget_entry.get('budgetFunds')['stages'][0]['endDate'][:-1]),
                        KBK = budget_entry.get('budgetFunds')['stages'][0]['payments'].get('KBK'),
                        paymentSumRUR=try_to_num(try_get_first(budget_entry.get('budgetFunds').get('stages')).get('payments').get('paymentSumRUR'), "float"),
                        name=budget_entry.get('budget').get('name'),
                        paymentYearMonth=date
                    )
                    bg.save()
                except django.db.utils.IntegrityError:
                    log('SAVE ID ERROR', False)
                contract_entry = entry.get('contract')
                try:
                    ct = Contract.objects.create(
                        id=contract_entry.get('_id'), 
                        contractUrl=contract_entry.get('contractUrl'), 
                        documentBase=contract_entry.get('documentBase'), 
                        startDate=datetime.fromisoformat(contract_entry.get('execution').get('startDate')[:-1]), 
                        endDate=datetime.fromisoformat(contract_entry['execution']['endDate'][:-1]), 
                        fz=try_to_num(contract_entry.get('fz'), "int"), 
                        price=try_to_num(contract_entry.get('price'), "decimal"), 
                        printFromUrl=contract_entry.get('printFormUrl'), 
                        protocolDate=try_to_date((contract_entry.get('protocolDate'))), 
                        publishDate=datetime.fromisoformat(contract_entry.get('publishDate')), 
                        signDate=datetime.fromisoformat(contract_entry['signDate'][:-1]), 
                        regionCode=try_to_num(contract_entry.get('regionCode'), "int"), 
                        scanUrl=contract_entry['scan'][0]['url'], 
                        budget=bg
                    )

                    customer_entry = contract_entry.get('customer')
                    try:
                        cm = Customer.objects.create(
                            inn = try_to_num(customer_entry.get('inn'), "int"),
                            fullName = customer_entry.get('fullName'),
                            kpp = try_to_num(customer_entry.get('kpp'), "int"),
                            postalAddress = customer_entry.get('postalAddress'),
                            regNum = try_to_num(customer_entry.get('regNum'), "int")
                        )
                        cm.save()
                        ct.customers.add(cm)
                    except django.db.utils.IntegrityError:
                        log('THE SAME CUSTOMER', False)
                    suppliers_entry = contract_entry.get('suppliers')
                    for supplier_entry in suppliers_entry:
                        try:
                            sp = Supplier.objects.create(
                                inn = try_to_num(supplier_entry.get('inn'), "int"),
                                kpp = try_to_num(supplier_entry.get('kpp'), "int"),
                                factualAddress = supplier_entry.get('factualAddress'),
                                organizationName = supplier_entry.get('organizationName'),
                                singularName = try_get_get(supplier_entry.get('legalForm'), 'singularName'),
                                middleName = try_get_get(supplier_entry.get('contactInfo'), 'middleName'),
                                lastName = try_get_get(supplier_entry.get('contactInfo'), 'lastName'),
                                firstName = try_get_get(supplier_entry.get('contactInfo'), 'firstName')
                            )
                            sp.save()
                            ct.suppliers.add(sp)
                        except django.db.utils.IntegrityError:
                            log('THE SAME SUPPLIER', False)
                    ct.save()
                
                    obj = Object.objects.create(
                        id=entry.get('_id'),
                        title=entry.get('title'),
                        region=try_to_num(entry.get('region'), "int"),
                        signDate=datetime.fromisoformat(entry.get('signDate')[:-1]),
                        contract=ct
                    )                
                    obj.save()
                
                    products_entry = contract_entry.get('products')
                    for product_entry in products_entry:
                        try:
                            pd = Product.objects.create(
                                sid = try_to_num(try_get_first(products_entry).get('sid'), "int"),
                                name = try_get_first(products_entry).get('name'),
                                price = try_to_num(try_get_first(products_entry).get('price'), "decimal"),
                                contract=ct
                            )
                            pd.save()
                        except django.db.utils.IntegrityError:
                            log('THE SAME PRODUCT', False)
                except django.db.utils.IntegrityError:
                    log('SAME ID!', False)
            print()
            print()
            print()
            log('THE END :)')

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

