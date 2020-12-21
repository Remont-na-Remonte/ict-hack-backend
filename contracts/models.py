from django.db import models

class Budget(models.Model):
    code = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    endDate = models.DateField()
    KBK = models.DecimalField(max_digits=21, decimal_places=0)
    paymentYearMonth = models.DateField()
    paymentSumRUR = models.DecimalField(max_digits=20, decimal_places=2)


class Customer(models.Model):
    inn = models.IntegerField(primary_key=True, editable=False)
    fullName = models.CharField(max_length=512)
    kpp = models.IntegerField()
    postalAddress = models.CharField(max_length=512)
    regNum = models.IntegerField()


class Supplier(models.Model):
    inn = models.IntegerField(primary_key=True, editable=False)
    kpp = models.IntegerField()
    factualAddress = models.CharField(max_length=1024)
    organizationName = models.CharField(max_length=1024)
    singularName = models.CharField(max_length=1024)
    middleName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=25)


class Contract(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    customers = models.ManyToManyField(Customer,related_name="customer_contract_type", through='Contract_Customer')
    suppliers = models.ManyToManyField(Customer, through='Contract_Supplier')
    contratUrl = models.URLField(max_length=200)
    documentBase = models.CharField(max_length=1024)
    startDate = models.DateField()
    endDate = models.DateField()
    fz = models.SmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    printFromUrl = models.URLField(max_length=200)
    protocolDate = models.DateField()
    publishDate = models.DateField()
    regionCode = models.SmallIntegerField()
    scanUrld = models.URLField(max_length=200)
    signDate = models.DateField()
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)


class Product(models.Model):
    sid = models.IntegerField(primary_key=True, editable=False)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=15, decimal_places=2)


class Object(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    title = models.CharField(max_length=200)
    region = models.SmallIntegerField()
    signDate = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Contract_Customer(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Contract_Supplier(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Section(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    mk = models.IntegerField()
    section_start = models.IntegerField()
    section_end = models.IntegerField()
    coordinates = models.JSONField()


class Road(models.Model):
    selections = models.ManyToManyField(Section, through='Section_Road')
    type = models.CharField(max_length=25)
    road_title = models.CharField(max_length=1024)


class Section_Road(models.Model):
    road = models.ForeignKey(Road, on_delete=models.CASCADE)
    selection = models.ForeignKey(Section, on_delete=models.CASCADE)
