from django.contrib import admin
from website.models import Product,Order,OrderItem,ShippingAddress

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)