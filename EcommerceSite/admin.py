from django.contrib import admin
from .models import Product,Order,OrderedProduct

admin.site.register(Product)
admin.site.register(OrderedProduct)
admin.site.register(Order)


# Register your models here.
