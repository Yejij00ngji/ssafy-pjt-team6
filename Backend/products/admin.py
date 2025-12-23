from django.contrib import admin
from .models import FinancialProduct, ProductOption

# # Register your models here.
admin.site.register(FinancialProduct)
admin.site.register(ProductOption)