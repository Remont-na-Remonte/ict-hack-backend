from django.contrib import admin
from contracts.models import Object, Contract, Budget, Product, Contract_Customer, Contract_Supplier, Customer, Supplier, Section, Road, Section_Road, Section_Contract

class AddAdmin(admin.ModelAdmin):
    budget_list_display = ['code ', 'name', 'endDate', 'KBK', 'paymentSumRUR'] 

admin.site.register(Object)
admin.site.register(Contract)
admin.site.register(Budget, AddAdmin)
admin.site.register(Product)
admin.site.register(Contract_Customer)
admin.site.register(Contract_Supplier)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Section)
admin.site.register(Road)
admin.site.register(Section_Road)
admin.site.register(Section_Contract)
