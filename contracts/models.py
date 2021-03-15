from django.db import models
from django.utils import timezone

class Budget(models.Model):
    code = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=1024, null=True)
    endDate = models.DateField(null=True)
    KBK = models.CharField(default="None", blank=True, max_length=64, null=True)
    paymentYearMonth = models.DateField(null=True, blank=False)
    paymentSumRUR = models.DecimalField(max_digits=20, decimal_places=2, null=True)


class Customer(models.Model):
    inn = models.BigIntegerField(primary_key=True, editable=False)
    fullName = models.CharField(max_length=512, null=True)
    kpp = models.IntegerField(null=True)
    postalAddress = models.CharField(max_length=512, null=True)
    regNum = models.BigIntegerField(null=True)


class Supplier(models.Model):
    inn = models.BigIntegerField(primary_key=True, editable=False)
    kpp = models.BigIntegerField(null=True)
    factualAddress = models.CharField(max_length=3025, null=True)
    organizationName = models.CharField(max_length=3026, null=True)
    singularName = models.CharField(max_length=3027, null=True)
    middleName = models.CharField(max_length=216, null=True)
    lastName = models.CharField(max_length=216, null=True)
    firstName = models.CharField(max_length=216, null=True)


class Contract(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    average_km_price = models.DecimalField(max_digits=16, decimal_places=5, null=True),
    customers = models.ManyToManyField(Customer,related_name="customer_contract_type", through='Contract_Customer')
    suppliers = models.ManyToManyField(Supplier, through='Contract_Supplier')
    contractUrl = models.URLField(max_length=5028, null=True)
    documentBase = models.CharField(max_length=5029, null=True)
    startDate = models.DateTimeField(default=timezone.now, null=True)
    endDate = models.DateTimeField(default=timezone.now, null=True)
    fz = models.SmallIntegerField(null=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    printFromUrl = models.URLField(max_length=500, null=True)
    protocolDate = models.DateTimeField(default=timezone.now, null=True)
    publishDate = models.DateTimeField(default=timezone.now, null=True)
    regionCode = models.SmallIntegerField(null=True)
    scanUrl = models.URLField(max_length=5034, null=True)
    signDate = models.DateTimeField(default=timezone.now, null=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)


class Product(models.Model):
    sid = models.BigIntegerField(primary_key=True, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    name = models.CharField(max_length=5049, null=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, null=True)


class Object(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    title = models.CharField(max_length=5048, null=True)
    region = models.SmallIntegerField(null=True)
    signDate = models.DateField(null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Contract_Customer(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Contract_Supplier(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)


class Section(models.Model):
    contracts = models.ManyToManyField(Contract, through='Section_Contract')
    km = models.IntegerField(null=True)
    section_start = models.IntegerField(null=True)
    section_end = models.IntegerField(null=True)
    coordinates = models.JSONField(null=True)


class Road(models.Model):
    sections = models.ManyToManyField(Section, through='Section_Road')
    type = models.CharField(max_length=94, null=True)
    road_title = models.CharField(max_length=5037, null=True)


class Section_Road(models.Model):
    road = models.ForeignKey(Road, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Section_Contract(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
