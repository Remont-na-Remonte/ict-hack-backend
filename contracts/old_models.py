from django.db import models

class Budget(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=200)
    endDate = models.DateField()
    KBK = models.DecimalField(max_digits=21, decimal_places=0)
    paymentYearMonth = models.DateField()
    paymentSumRUR = models.

class Contract(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    contratUrl = models.URLField(max_length=200)
    documentBase = models.CharField(max_length=1024)
    startDate = models.DateField()
    endDate = models.DateField()
    fz = models.SmallIntegerField()
    price = models.DecimalField(max_digiths=15, 2)
    printFromUrl = models.URLField(max_length=200)
    protocolDate = models.DateField()
    publishDate = models.DateField()
    regionCode = models.SmallIntegerField()
    scanUrld = models.URLField(max_length=200)
    signDate = models.DateField()
    budget_code = models.ForeignKey(, on_delete=models.CASCADE) #TODO

class Object(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    title = models.CharField(max_length=200)
    region = models.SmallIntegerField()
    signDate = models.DateField()
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)

